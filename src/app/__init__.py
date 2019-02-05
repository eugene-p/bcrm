from flask import Flask
from app.core import init_core

def create_app():
    app = Flask(__name__)
    init_core(app)
    return app
