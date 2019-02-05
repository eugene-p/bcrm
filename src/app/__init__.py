from flask import Flask
from app.core import core_api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(core_api)
    return app