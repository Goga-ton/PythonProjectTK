from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"

from DZ_VD06_app import routes

