# coding: utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

"""
    BCRM core api
    ========================
    File contains api for
     - EntityType
"""
from app.core.resources import core_api
from app.core.db import init_db

def init_core(app):
    init_db(app)
    app.register_blueprint(core_api)
