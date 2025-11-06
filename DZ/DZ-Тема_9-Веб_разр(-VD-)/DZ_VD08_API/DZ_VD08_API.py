from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    citata = None
    if request.method == 'POST':
        citata = get_citata()
    return render_template('DZ_VD08_index.html', citata=citata)

def get_citata():
    url=f"https://zenquotes.io/api/random"
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
4566


