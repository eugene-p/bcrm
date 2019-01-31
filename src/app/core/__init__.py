# coding: utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

"""
    BCRM core api
    ========================
    File contains api for
     - EntityType
"""
import uuid
from flask import Blueprint, jsonify, request, make_response
from app.decorators.rest import validate_payload_is_json, validate_payload_with_schema

core_api = Blueprint('core_api', __name__, url_prefix='/api')

entity_types = [
    {
        'id': 'db5e8763-5568-4c02-9245-4e79a68e8127',
        'name': u'company',
        'schema': {}
    }
]

entity_post_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "schema": {"type": "object"},
    },
    "required": [ "name", "schema" ],
}

def get_by_id(entity_type_id):
    return [entity_type for entity_type in entity_types if entity_type['id'] == entity_type_id]


@core_api.route('/entity-types', methods=['GET'])
def get_entity_types():
    return jsonify({'entity-types': entity_types})


@core_api.route('/entity-types/<string:entity_type_id>', methods=['GET'])
def get_entity_type_by_id(entity_type_id):
    entity_type = get_by_id(entity_type_id)
    if(len(entity_type) == 0):
        return make_response(jsonify({'message': 'Not found'}), 404)
    return jsonify(entity_type[0])

@core_api.route('/entity-types', methods=['POST'])
@validate_payload_is_json
@validate_payload_with_schema(entity_post_schema)
def create_entity_type():
    entity_type = {
        'id': str(uuid.uuid4()),
        'name': request.json['name'],
        'schema': request.json['schema']
    }
    entity_types.append(entity_type)
    return jsonify(entity_type), 201

@core_api.route('/entity-types/<string:entity_type_id>', methods=['PUT'])
@validate_payload_is_json
@validate_payload_with_schema(entity_post_schema)
def update_entity_type(entity_type_id):
    entity_type = get_by_id(entity_type_id)
    if(len(entity_type) == 0):
        return make_response(jsonify({'message': 'Not found'}), 404)
    entity_type[0]['name'] = request.json['name']
    entity_type[0]['schema'] = request.json['schema']
    return jsonify(entity_type[0])

@core_api.route('/entity-types/<string:entity_type_id>', methods=['DELETE'])
def delete_entity_type(entity_type_id):
    entity_type = get_by_id(entity_type_id)
    if(len(entity_type) == 0):
        return make_response(jsonify({'message': 'Not found'}), 404)
    entity_types.remove(entity_type[0])
    return jsonify({'acknowledge': True})
