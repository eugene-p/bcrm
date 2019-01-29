from flask import Flask
from app.core import core_api

app = Flask(__name__)
app.register_blueprint(core_api)
