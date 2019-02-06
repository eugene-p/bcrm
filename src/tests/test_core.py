# coding: utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
"""
Core Api Tests
==============
"""
import json

def create_entity_type(client, name):
    entity_type_stub = {
        'name': name,
        'schema': { "test": "test"}
    }
    response = client.post('/api/entity-types',
        data=json.dumps(entity_type_stub),
        content_type='application/json')
    json_data = response.get_json()
    if response.status_code != 201:
        raise('error creating entity')
    return json_data['id']

def test_create_entity_type_success(client):
    """
    Tests that entity types can be created
    """
    entity_type_stub = {
        'name': u'test_create_entity_type_success',
        'schema': { "test": "test"}
    }
    response = client.post('/api/entity-types',
        data=json.dumps(entity_type_stub),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['name'] == 'test_create_entity_type_success'
    assert json_data['schema'] == { "test": "test"}

def test_create_entity_type_already_exists(client):
    """
    Tests that entity types creation fail if entity already exists
    """
    create_entity_type(client, 'test_create_entity_type_already_exists')
    entity_type_stub = {
        'name': u'test_create_entity_type_already_exists',
        'schema': { "test": "test"}
    }
    response = client.post('/api/entity-types',
        data=json.dumps(entity_type_stub),
        content_type='application/json')
    assert response.status_code == 404

def test_create_entity_types_content_type_not_json(client):
    """
    Tests that entity types return error when content type is not json
    """
    payload = {
        'name': u'test',
        'schema': {}
    }

    response = client.post('/api/entity-types',
        data=json.dumps(payload),
        content_type='application/text')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['message'] == 'payload is not json'

def test_create_entity_types_schema_not_valid(client):
    """
    Tests that entity types return error if schema is not valid
    """
    payload = {
        'test': u'test',
        'schema': {}
    }

    response = client.post('/api/entity-types',
        data=json.dumps(payload),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['message'] == "'name' is a required property"

def test_get_entity_type_by_id_success(client):
    """
    Tests that get entity type by id return 1 entity type
    """
    entity_type_id = create_entity_type(client, 'test_get_entity_type_by_id_success')
    response = client.get("/api/entity-types/{id}".format(id=entity_type_id))
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['id'] == entity_type_id
    assert json_data['name'] == "test_get_entity_type_by_id_success"
    assert json_data['schema'] == { "test": "test"}

def test_get_entity_type_by_id_not_found(client):
    """
    Tests that get entity type by id return 404 if not found
    """
    response = client.get('/api/entity-types/blah')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['message'] == 'Not found'

def test_update_entity_type_success(client):
    """
    Tests that entity types can be updated
    """
    entity_type_id = create_entity_type(client, 'test_update_entity_type_success')

    payload = {
        'name': u'test_update_entity_type_success_updated',
        'schema': { "test": "test"}
    }

    response = client.put("/api/entity-types/{id}".format(id=entity_type_id),
        data=json.dumps(payload),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['name'] == 'test_update_entity_type_success_updated'
    assert json_data['schema']['test'] == 'test'

def test_update_entity_type_not_json(client):
    """
    Tests that update entity type return error when content type is not json
    """
    payload = {
        'name': u'test',
        'schema': {
            "test": "test"
        }
    }

    response = client.put('/api/entity-types/db5e8763-5568-4c02-9245-4e79a68e812a',
        data=json.dumps(payload),
        content_type='application/text')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['message'] == 'payload is not json'

def test_update_entity_type_not_found(client):
    """
    Tests that update entity type return error when content type is not json
    """
    payload = {
        'name': u'test',
        'schema': {
            "test": "test"
        }
    }

    response = client.put('/api/entity-types/blah',
        data=json.dumps(payload),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['message'] == 'Not found'

def test_update_entity_type_schema_not_valid(client):
    """
    Tests that entity types can be updated
    """
    payload = {
        'name': u'test',
        'test': {
            "test": "test"
        }
    }

    response = client.put('/api/entity-types/db5e8763-5568-4c02-9245-4e79a68e812a',
        data=json.dumps(payload),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['message'] == "'schema' is a required property"

def test_delete_entity_type_success(client):
    """
    Tests that entity types can be deleted
    """
    entity_type_id = create_entity_type(client, 'test_delete_entity_type_success')

    response = client.delete("/api/entity-types/{id}".format(id=entity_type_id))
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['acknowledge'] == True

def test_delete_entity_type_not_found(client):
    """
    Tests that entity types can be deleted
    """
    entity_type_id = 'blah'
    response = client.delete('/api/entity-types/' + entity_type_id)
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['message'] == 'Not found'