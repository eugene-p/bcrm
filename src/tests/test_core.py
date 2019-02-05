
import json
from unittest import mock
from unittest.mock import patch


def test_get_entity(client):
    """
    Test get entity-types return a list of entity types
    """
    response = client.get('/api/entity-types')
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data['entity-types'], list)

entity_types = [
    {
        'id': 'db5e8763-5568-4c02-9245-4e79a68e812a',
        'name': u'company',
        'schema': {}
    }
]

def test_get_entity_type_by_id_success(client):
    """
    Tests that get entity type by id return 1 entity type
    """
    with patch('app.core.entity_types', entity_types):
        response = client.get('/api/entity-types/db5e8763-5568-4c02-9245-4e79a68e812a')
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data['id'] == "db5e8763-5568-4c02-9245-4e79a68e812a"
        assert json_data['name'] == "company"
        assert json_data['schema'] == {}

def test_get_entity_type_by_id_not_found(client):
    """
    Tests that get entity type by id return 404 if not found
    """
    with patch('app.core.entity_types', entity_types):
        response = client.get('/api/entity-types/blah')
        json_data = response.get_json()
        assert response.status_code == 404
        assert json_data['message'] == 'Not found'

def test_create_entity_type_success(client):
    """
    Tests that entity types can be created
    """
    with patch('app.core.entity_types', entity_types):
        payload = {
            'name': u'test',
            'schema': {}
        }

        response = client.post('/api/entity-types',
            data=json.dumps(payload),
            content_type='application/json')
        json_data = response.get_json()
        assert response.status_code == 201
        assert json_data['name'] == 'test'
        assert json_data['schema'] == {}
        assert len(entity_types) == 2

def test_create_entity_types_content_type_not_json(client):
    """
    Tests that entity types return error when content type is not json
    """
    with patch('app.core.entity_types', entity_types):
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
    with patch('app.core.entity_types', entity_types):
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

def test_update_entity_type_success(client):
    """
    Tests that entity types can be updated
    """
    with patch('app.core.entity_types', entity_types):
        payload = {
            'name': u'test',
            'schema': {
                "test": "test"
            }
        }

        response = client.put('/api/entity-types/db5e8763-5568-4c02-9245-4e79a68e812a',
            data=json.dumps(payload),
            content_type='application/json')
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data['name'] == 'test'
        assert json_data['schema']['test'] == 'test'

def test_update_entity_type_not_json(client):
    """
    Tests that update entity type return error when content type is not json
    """
    with patch('app.core.entity_types', entity_types):
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
    with patch('app.core.entity_types', entity_types):
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
    with patch('app.core.entity_types', entity_types):
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
    with patch('app.core.entity_types', entity_types):
        entity_type_id = 'db5e8763-5568-4c02-9245-4e79a68e812a'
        response = client.delete('/api/entity-types/' + entity_type_id)
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data['acknowledge'] == True
        entity_type = [entity_type for entity_type in entity_types if entity_type['id'] == entity_type_id]
        assert len(entity_type) == 0

def test_delete_entity_type_not_found(client):
    """
    Tests that entity types can be deleted
    """
    with patch('app.core.entity_types', entity_types):
        entity_type_id = 'blah'
        response = client.delete('/api/entity-types/' + entity_type_id)
        json_data = response.get_json()
        assert response.status_code == 404
        assert json_data['message'] == 'Not found'