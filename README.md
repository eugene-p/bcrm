# bcrm

[![Maintainability](https://api.codeclimate.com/v1/badges/c786ce57567ecefe0fb6/maintainability)](https://codeclimate.com/github/skalpel-tech/bcrm/maintainability)

Open Source Business CRM Solution

## docker

Run the application in docker

```bash
docker-compose up --build
```

## developement

Create a virtual environment

```bash
mkvirtualenv bcrm
```

Install the dependencies

```bash
cd src
pip install -r requirements.txt
```

Set the flask app root

```bash
FLASK_APP=app
```

Run the application

```bash
flask run
```

import [postman collection](postman/BCRM.postman_collection.json)  [postman environment](postman/BCRM.postman_environment.json)

or start building an application: [swagger](docs\BCRM.swagger.yml)

## Tests

Install tests dependencies

```bash
pip install -r tests/requirements.txt
```

Run the tests

```bash
pytest
```

Run with coverage report::

```
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
```
