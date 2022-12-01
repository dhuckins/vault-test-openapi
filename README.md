# vault-test-openapi

test [Hashicorp vault](https://www.vaultproject.io/) openapi spec
with [Schemathesis](https://schemathesis.readthedocs.io/en/stable/)

## Running tests

set up a virtual environment if you don't already have one

```shell
$ python3.10 -m venv .venv
$ source ./.venv/bin/activate
```

install dependencies
```shell
(.venv) $ python -m pip install requirements.in  # or the frozen requirements.txt
```

run the test(s)
```shell
(.venv) $ python -m pytest --html=htmlcov/pytest/index.html --self-contained-html
```

A test report has been generated, start a dev server
```shell
(.venv) $ python -m http.server
```

View the report by going to [localhost:8000/htmlcov/pytest](http://localhost:8000/htmlcov/pytest) in your browser
