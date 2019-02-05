# coding: utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import os
import click
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
db = SQLAlchemy(session_options={'autocommit': True})
def init_db(app):

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('') \
        or 'sqlite:///bcrm.db' # Creates bcrm.db inside of app folder

    db.init_app(app)
    app.cli.add_command(init_db_command)

def create_db():
    db.create_all()
    pass

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    create_db()
    click.echo('Initialized the database.')