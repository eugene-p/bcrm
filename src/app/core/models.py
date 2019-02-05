# coding: utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import datetime
import uuid
import json
from app.core.db import db

entity_post_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "schema": {"type": "object"},
    },
    "required": [ "name", "schema" ],
}

class EntityType(db.Model):
    """ **EntityType** db model """

    __tablename__ = 'entity_type'

    id = db.Column(
        db.String(length=60),
        unique=True,
        nullable=False,
        primary_key=True
    )

    name = db.Column(
        db.String(length=80),
        unique=True,
        nullable=False,
        default=''
    )

    schema = db.Column(
        db.Text(),
        nullable=False
    )

    def __init__(self, **kwargs):
        self.id = uuid.uuid4().__str__()
        self.name = kwargs.get('name')
        self.schema = json.dumps(kwargs.get('schema'))

    def toDict(self):
        data = dict([])
        data['id'] = self.id
        data['name'] = self.name
        data['schema'] = json.loads(self.schema)
        return data
