# coding: utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
'''
Entity Types Api Tests
==============
'''
import json
from test_entity_types import create_entity_type

entity_stub = {
    'entity_type_id': 'test_entity_type_id',
    'content': {'content':'content'}
}

def create_entity(client, entity_type_name):
    stub = {
        'entity_type_id': create_entity_type(client, entity_type_name),
        'content': entity_stub['content']
    }

    response = client.post('/api/entities',
        data=json.dumps(stub),
        content_type='application/json')
    json_data = response.get_json()
    if response.status_code != 201:
        raise TypeError('error creating entity')
    return json_data['id']


def test_create_entity_success(client):
    create_entity(client, 'test_entity_type_name')

def test_create_entity_invalid_content(client):
    stub = {
        'entity_type_id': create_entity_type(client, 'test_entity_type_name--invalid_content'),
        'content': {'crap': 'crap'}
    }

    response = client.post('/api/entities',
        data=json.dumps(stub),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['message'] == "Entity content does not match type schema"

def test_create_entity_invalid_entity_type(client):
    response = client.post('/api/entities',
        data=json.dumps(entity_stub),
        content_type='application/json')
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == "Entity type id '{}' does not exist".format(entity_stub['entity_type_id'])

def test_create_entity_not_json(client):

    response = client.post('/api/entities',
        data=json.dumps(entity_stub),
        content_type='application/text')
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == 'payload is not json'

def test_create_entity_no_entity_type(client):

    stub = {
        'content': {'content':'content'}
    }

    response = client.post('/api/entities',
        data=json.dumps(stub),
        content_type='application/json')
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == "'entity_type_id' is a required property"

def test_create_entity_no_content(client):
    stub = {
        'entity_type_id': 'entity_type_id'
    }

    response = client.post('/api/entities',
        data=json.dumps(stub),
        content_type='application/json')
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == "'content' is a required property"

def test_create_entity_no_content_not_object(client):
    stub = {
        'entity_type_id': 'entity_type_id',
        'content': 'content'
    }

    response = client.post('/api/entities',
        data=json.dumps(stub),
        content_type='application/json')
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data['message'] == "'content' is not of type 'object'"

def test_get_entity_by_id(client):
    entity_id = create_entity(client, 'test_get_entity--entity_type_name')
    response = client.get('/api/entities/{}'.format(entity_id))
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['content'] == entity_stub['content']

def test_get_entity_by_id_fail(client):
    response = client.get('/api/entities/unknown')
    json_data = response.get_json()

    assert response.status_code == 404
    assert json_data['message'] == "Not found"

def test_delete_entity_by_id(client):
    entity_id = create_entity(client, 'test_delete_entity--entity_type_name')
    response = client.delete('/api/entities/{}'.format(entity_id))
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['acknowledge'] == True

def test_delete_entity_by_id_not_found(client):
    response = client.delete('/api/entities/not_found')
    json_data = response.get_json()

    assert response.status_code == 404
    assert json_data['message'] == 'Not found'

def test_update_entity_success(client):
    '''
    Tests that entity types can be updated
    '''

    name = 'test_update_entity_success'
    entity_id = create_entity(client, name)
    entity_type_id = create_entity_type(client, name + '_updated')

    payload = {
        'entity_type_id': entity_type_id,
        'content': {'test': 'new test'}
    }

    response = client.put('/api/entities/{}'.format(entity_id),
        data=json.dumps(payload),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['entity_type_id'] == entity_type_id
    assert json_data['content'] == {'test': 'new test'}

def test_update_entity_invalid_type(client):
    '''
    Tests that entity types can be updated
    '''

    name = 'test_update_entity_invalid_type'
    entity_id = create_entity(client, name)

    payload = {
        'entity_type_id': name + '_no',
        'content': {'test': 'new test'}
    }

    response = client.put('/api/entities/{}'.format(entity_id),
        data=json.dumps(payload),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['message'] == "Entity type id '{}' does not exist".format(name+'_no')

def test_update_entity_not_found(client):
    '''
    Tests that entity types can be updated
    '''

    payload = {
        'entity_type_id': 'test_update_entity_not_found',
        'content': {'test': 'new test'}
    }

    response = client.put('/api/entities/nope',
        data=json.dumps(payload),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['message'] == 'Not found'


def test_update_entity_invalid_content(client):
    '''
    Tests that entity types can be updated
    '''
    name = 'test_update_entity_invalid_content'
    entity_id = create_entity(client, name)
    entity_type_id = create_entity_type(client, name + '_updated')

    payload = {
        'entity_type_id': entity_type_id,
        'content': {'crap': 'crap'}
    }

    response = client.put('/api/entities/{}'.format(entity_id),
        data=json.dumps(payload),
        content_type='application/json')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['message'] == 'Entity content does not match type schema'
