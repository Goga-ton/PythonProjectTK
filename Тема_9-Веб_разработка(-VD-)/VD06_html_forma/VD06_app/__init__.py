from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"

from VD06_app import routes

