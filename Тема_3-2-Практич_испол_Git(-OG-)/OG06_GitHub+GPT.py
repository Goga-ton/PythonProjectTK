import base64
from typing import Any, Dict, List, Optional

import requests
from flask import Flask, jsonify, request

import config

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com"


# ======================
# ВСПОМОГАТЕЛЬНОЕ
# ======================

def github_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def github_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
) -> requests.Response:
    url = f"{GITHUB_API_URL}{endpoint}"
    return requests.request(
        method=method,
        url=url,
        headers=github_headers(),
        params=params,
        json=json_data,
        timeout=30,
    )


def validate_repo(repo: Optional[str]) -> Optional[str]:
    if not repo:
        return "repo is required"

    if hasattr(config, "ALLOWED_REPOS") and config.ALLOWED_REPOS:
        if repo not in config.ALLOWED_REPOS:
            return f"repo '{repo}' is not allowed"

    return None


# ======================
# TREE
# ======================

def build_tree_structure(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    root = {"type": "dir", "name": "", "path": "", "children": {}}

    for item in items:
        path = item["path"]
        item_type = item["type"]
        parts = path.split("/")
        current = root

        for i, part in enumerate(parts):
            is_last = i == len(parts) - 1

            if not is_last:
                if part not in current["children"]:
                    current["children"][part] = {
                        "type": "dir",
                        "name": part,
                        "path": "/".join(parts[: i + 1]),
                        "children": {},
                    }
                current = current["children"][part]
            else:
                if item_type == "tree":
                    current["children"][part] = {
                        "type": "dir",
                        "name": part,
                        "path": path,
                        "children": {},
                    }
                else:
                    current["children"][part] = {
                        "type": "file",
                        "name": part,
                        "path": path,
                        "size": item.get("size"),
                        "sha": item.get("sha"),
                    }

    return convert_children(root)


def convert_children(node: Dict[str, Any]) -> Dict[str, Any]:
    if node["type"] == "dir":
        children = list(node["children"].values())
        children.sort(key=lambda x: (x["type"] != "dir", x["name"].lower()))
        node["children"] = [convert_children(child) for child in children]
    return node


# ======================
# ENDPOINTS
# ======================

@app.route("/repo/tree", methods=["GET"])
def get_repo_tree() -> Any:
    repo = request.args.get("repo")
    branch = request.args.get("branch", "main")

    error = validate_repo(repo)
    if error:
        return jsonify({"error": error}), 400

    # получаем SHA
    branch_resp = github_request(
        "GET", f"/repos/{config.GITHUB_USER}/{repo}/branches/{branch}"
    )
    if branch_resp.status_code != 200:
        return jsonify(branch_resp.json()), branch_resp.status_code

    tree_sha = branch_resp.json()["commit"]["commit"]["tree"]["sha"]

    # получаем дерево
    tree_resp = github_request(
        "GET",
        f"/repos/{config.GITHUB_USER}/{repo}/git/trees/{tree_sha}",
        params={"recursive": "1"},
    )
    if tree_resp.status_code != 200:
        return jsonify(tree_resp.json()), tree_resp.status_code

    items = tree_resp.json().get("tree", [])
    structured = build_tree_structure(items)

    return jsonify(structured["children"]), 200


@app.route("/repo/file", methods=["GET"])
def get_file() -> Any:
    repo = request.args.get("repo")
    path = request.args.get("path")
    branch = request.args.get("branch", "main")

    error = validate_repo(repo)
    if error:
        return jsonify({"error": error}), 400

    if not path:
        return jsonify({"error": "path is required"}), 400

    resp = github_request(
        "GET",
        f"/repos/{config.GITHUB_USER}/{repo}/contents/{path}",
        params={"ref": branch},
    )

    if resp.status_code != 200:
        return jsonify(resp.json()), resp.status_code

    data = resp.json()

    content = data.get("content", "")
    if data.get("encoding") == "base64":
        content = base64.b64decode(content).decode("utf-8", errors="replace")

    return jsonify({
        "path": path,
        "content": content,
        "sha": data.get("sha"),
    })


@app.route("/repo/file", methods=["POST"])
def create_file() -> Any:
    payload = request.get_json()

    repo = payload.get("repo")
    path = payload.get("path")
    content = payload.get("content")
    branch = payload.get("branch", "main")

    error = validate_repo(repo)
    if error:
        return jsonify({"error": error}), 400

    if not path or content is None:
        return jsonify({"error": "path and content required"}), 400

    # проверка существования
    check = github_request(
        "GET",
        f"/repos/{config.GITHUB_USER}/{repo}/contents/{path}",
        params={"ref": branch},
    )

    if check.status_code == 200:
        return jsonify({"error": "file already exists"}), 409

    encoded = base64.b64encode(content.encode()).decode()

    resp = github_request(
        "PUT",
        f"/repos/{config.GITHUB_USER}/{repo}/contents/{path}",
        json_data={
            "message": f"Create {path}",
            "content": encoded,
            "branch": branch,
        },
    )

    if resp.status_code not in (200, 201):
        return jsonify(resp.json()), resp.status_code

    return jsonify({
        "message": "created",
        "path": path
    }), 201


@app.route("/health")
def health():
    return jsonify({"status": "ok", "user": config.GITHUB_USER})

def get_file_content_from_github(repo: str, path: str, branch: str = "main") -> Dict[str, Any]:
    resp = github_request(
        "GET",
        f"/repos/{config.GITHUB_USER}/{repo}/contents/{path}",
        params={"ref": branch},
    )

    if resp.status_code != 200:
        return {
            "path": path,
            "error": "failed to fetch file",
            "details": resp.json(),
        }

    data = resp.json()
    content = data.get("content", "")

    if data.get("encoding") == "base64":
        content = base64.b64decode(content).decode("utf-8", errors="replace")

    return {
        "path": path,
        "sha": data.get("sha"),
        "size": data.get("size"),
        "content": content,
    }

@app.route("/repo/files-content", methods=["GET"])
def get_all_files_content() -> Any:
    repo = request.args.get("repo")
    branch = request.args.get("branch", "main")

    error = validate_repo(repo)
    if error:
        return jsonify({"error": error}), 400

    branch_resp = github_request(
        "GET",
        f"/repos/{config.GITHUB_USER}/{repo}/branches/{branch}"
    )
    if branch_resp.status_code != 200:
        return jsonify(branch_resp.json()), branch_resp.status_code

    tree_sha = branch_resp.json()["commit"]["commit"]["tree"]["sha"]

    tree_resp = github_request(
        "GET",
        f"/repos/{config.GITHUB_USER}/{repo}/git/trees/{tree_sha}",
        params={"recursive": "1"},
    )
    if tree_resp.status_code != 200:
        return jsonify(tree_resp.json()), tree_resp.status_code

    tree_items = tree_resp.json().get("tree", [])
    file_items = [item for item in tree_items if item.get("type") == "blob"]

    result = []
    for item in file_items:
        file_data = get_file_content_from_github(
            repo=repo,
            path=item["path"],
            branch=branch,
        )
        result.append(file_data)

    return jsonify({
        "repo": repo,
        "branch": branch,
        "files_count": len(result),
        "files": result,
    }), 200

@app.route("/repo/file", methods=["PUT"])
def update_file() -> Any:
    payload = request.get_json()

    repo = payload.get("repo")
    path = payload.get("path")
    content = payload.get("content")
    branch = payload.get("branch", "main")
    commit_message = payload.get("commit_message", f"Update {path}")

    error = validate_repo(repo)
    if error:
        return jsonify({"error": error}), 400

    if not path or content is None:
        return jsonify({"error": "path and content required"}), 400

    check_resp = github_request(
        "GET",
        f"/repos/{config.GITHUB_USER}/{repo}/contents/{path}",
        params={"ref": branch},
    )

    if check_resp.status_code == 404:
        return jsonify({"error": f"file not found: {path}"}), 404

    if check_resp.status_code != 200:
        return jsonify(check_resp.json()), check_resp.status_code

    file_data = check_resp.json()
    file_sha = file_data.get("sha")

    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    update_resp = github_request(
        "PUT",
        f"/repos/{config.GITHUB_USER}/{repo}/contents/{path}",
        json_data={
            "message": commit_message,
            "content": encoded_content,
            "sha": file_sha,
            "branch": branch,
        },
    )

    if update_resp.status_code not in (200, 201):
        return jsonify(update_resp.json()), update_resp.status_code

    return jsonify({
        "message": "updated",
        "path": path,
        "branch": branch,
    }), 200

@app.route("/repo/file", methods=["DELETE"])
def delete_file() -> Any:
    payload = request.get_json()

    repo = payload.get("repo")
    path = payload.get("path")
    branch = payload.get("branch", "main")
    commit_message = payload.get("commit_message", f"Delete {path}")

    error = validate_repo(repo)
    if error:
        return jsonify({"error": error}), 400

    if not path:
        return jsonify({"error": "path required"}), 400

    check_resp = github_request(
        "GET",
        f"/repos/{config.GITHUB_USER}/{repo}/contents/{path}",
        params={"ref": branch},
    )

    if check_resp.status_code == 404:
        return jsonify({"error": f"file not found: {path}"}), 404

    if check_resp.status_code != 200:
        return jsonify(check_resp.json()), check_resp.status_code

    file_data = check_resp.json()
    file_sha = file_data.get("sha")

    delete_resp = github_request(
        "DELETE",
        f"/repos/{config.GITHUB_USER}/{repo}/contents/{path}",
        json_data={
            "message": commit_message,
            "sha": file_sha,
            "branch": branch,
        },
    )

    if delete_resp.status_code != 200:
        return jsonify(delete_resp.json()), delete_resp.status_code

    return jsonify({
        "message": "deleted",
        "path": path,
        "branch": branch,
    }), 200

if __name__ == "__main__":
    app.run(debug=True)