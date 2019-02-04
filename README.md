# bcrm

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/20080db98c8b42fdb0db9b4718dd20d4)](https://app.codacy.com/app/cedar-technologies/bcrm?utm_source=github.com&utm_medium=referral&utm_content=skalpel-tech/bcrm&utm_campaign=Badge_Grade_Dashboard)

Open Source Business CRM Solution

# developement

Create a virtual environment

```bash
mkvirtualenv bcrm
```

Install the dependencies

```
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