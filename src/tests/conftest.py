# coding: utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
"""
Test Fixtures
=============
"""
import os
import pytest

from app import create_app
from app.core.db import db as _db

@pytest.fixture(scope='session')
def app():
    """Session-wide test `Flask` application."""

    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
    )

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()
    ctx.pop()

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """Session-wide test database."""
 
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
