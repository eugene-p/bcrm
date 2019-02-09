import uuid
import json
from flask import Blueprint, jsonify, request, make_response
from jsonschema import validate, ValidationError
from sqlalchemy.exc import IntegrityError
from app.decorators.rest import validate_payload_is_json, validate_payload_with_schema
from app.core.models.entity import Entity, entity_schema
from app.core.models.entity_type import EntityType, entity_type_schema

from app.core.db import db

core_api = Blueprint('core_api', __name__, url_prefix='/api')
@core_api.route('/entity-types/<string:entity_type_id>', methods=['GET'])
def get_entity_type_by_id(entity_type_id):
    entity_type = EntityType.query.get(entity_type_id)
    if not entity_type:
        return make_response(jsonify({'message': 'Not found'}), 404)

    return jsonify(entity_type.toDict())

@core_api.route('/entity-types', methods=['POST'])
@validate_payload_is_json
@validate_payload_with_schema(entity_type_schema)
def create_entity_type():

    entity_type = EntityType(
        schema=request.json['schema'],
        name=request.json['name']
    )

    db.session.begin()
    db.session.add(entity_type)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(
            jsonify({'message': "Entity Type '{}' is not unique".format(entity_type.name)}),
            409
        )
    return jsonify(entity_type.toDict()), 201

@core_api.route('/entity-types/<string:entity_type_id>', methods=['PUT'])
@validate_payload_is_json
@validate_payload_with_schema(entity_type_schema)
def update_entity_type(entity_type_id):
    entity_type = EntityType.query.get(entity_type_id)
    if not entity_type:
        return make_response(jsonify({'message': 'Not found'}), 404)

    db.session.begin()
    entity_type.name = request.json['name']
    entity_type.schema = json.dumps(request.json['schema'])
    db.session.commit()
    return jsonify(entity_type.toDict())

@core_api.route('/entity-types/<string:entity_type_id>', methods=['DELETE'])
def delete_entity_type(entity_type_id):
    entity_type = EntityType.query.get(entity_type_id)
    if not entity_type:
        return make_response(jsonify({'message': 'Not found'}), 404)

    db.session.begin()
    db.session.delete(entity_type)
    db.session.commit()
    return jsonify({'acknowledge': True})


@core_api.route('/entities/<string:entity_id>', methods=['GET'])
def get_entity_by_id(entity_id):
    entity = Entity.query.get(entity_id)
    if not entity:
        return make_response(jsonify({'message': 'Not found'}), 404)

    return jsonify(entity.toDict())

@core_api.route('/entities', methods=['POST'])
@validate_payload_is_json
@validate_payload_with_schema(entity_schema)
def create_entity():
    entity_type_id = request.json['entity_type_id']
    content = request.json['content']
    entity_type = EntityType.query.get(entity_type_id)
    if not entity_type:
        return make_response(
            jsonify({'message': "Entity type id '{}' does not exist".format(entity_type_id)}),
            400
        )

    try:
        validate(instance=content, schema=entity_type.toDict()['schema'])
    except ValidationError:
        return make_response(
            jsonify({'message': "Entity content does not match type schema"}),
            400
        )

    entity = Entity(
        entity_type_id=entity_type_id,
        content=content
    )

    db.session.begin()
    db.session.add(entity)
    
    db.session.commit()
    return jsonify(entity.toDict()), 201

@core_api.route('/entities/<string:entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    entity = Entity.query.get(entity_id)
    if not entity:
        return make_response(jsonify({'message': 'Not found'}), 404)

    db.session.begin()
    db.session.delete(entity)
    db.session.commit()
    return jsonify({'acknowledge': True})


@core_api.route('/entities/<string:entity_id>', methods=['PUT'])
@validate_payload_is_json
@validate_payload_with_schema(entity_schema)
def update_entity(entity_id):
    entity = Entity.query.get(entity_id)
    if not entity:
        return make_response(jsonify({'message': 'Not found'}), 404)

    entity_type_id = request.json['entity_type_id']
    content = request.json['content']
    entity_type = EntityType.query.get(entity_type_id)
    if not entity_type:
        return make_response(
            jsonify({'message': "Entity type id '{}' does not exist".format(entity_type_id)}),
            400
        )

    try:
        validate(instance=content, schema=entity_type.toDict()['schema'])
    except ValidationError:
        return make_response(
            jsonify({'message': "Entity content does not match type schema"}),
            400
        )

    db.session.begin()
    entity.entityTypeId = entity_type_id
    entity.content = json.dumps(content)
    db.session.commit()
    return jsonify(entity.toDict())
