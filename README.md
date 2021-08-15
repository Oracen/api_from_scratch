# REPLACE_ME

## Installation
Installing this project will require some kind of system install of Python3 to install Poetry. Assume Python3 is the default system version. Then, run one of the following commands to install Poetry:
#### Linux/MacOS/WSL
```curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -```
#### Windows
```(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -```

Further information available [here](https://python-poetry.org/docs/).

Run install commands from the project root directory (i.e. the directory containing this doc)
`poetry install`
`poetry run mypy --install-types`

## Commands
Run all commands from the root directory

### Serve API
`poetry run uvicorn REPLACE_ME.api.main:app --reload --port=8000`

This will run the api on `localhost:8000` by default but this protects against envs. The path `/docs` can be used to inspect datatypes

### Run tests
`poetry run pytest`

### Check coverage
`poetry run coverage run -m pytest && poetry run coverage report -m`

### Check type assertions
`poetry run mypy .`

Given that writing type stubs for all the types is time consuming, consider running the following command instead:

`poetry run mypy . --ignore-missing-imports`