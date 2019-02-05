import uuid
import json
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy.exc import IntegrityError
from app.decorators.rest import validate_payload_is_json, validate_payload_with_schema
from app.core.models import EntityType, entity_post_schema
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
@validate_payload_with_schema(entity_post_schema)
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
        return make_response(
            jsonify({'message': "Entity Type '{}' is not unique".format(entity_type.name)}),
            404
        )
    return jsonify(entity_type.toDict()), 201

@core_api.route('/entity-types/<string:entity_type_id>', methods=['PUT'])
@validate_payload_is_json
@validate_payload_with_schema(entity_post_schema)
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
