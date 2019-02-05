# coding: utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def init_db(app):

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('') \
        or 'sqlite://test.db'

    db.init_app(app)

def create_db():
    pass