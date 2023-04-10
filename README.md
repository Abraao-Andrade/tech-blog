# THIAGO-DOMINGOS PROJECT

# Instalation

- Clone the repository;
- Go to the projects local folder;
- Start a virtual environment: `virtualenv -p python3.11 venv`;
- Activate venv `source venv/bin/activate`;
- Install Poetry lib manager: `pip install poetry`;
- Install libs: `poetry install`
- Run `pre-commit install` to make sure you are following the code style guide;
- Install PostgreeSQL and create database
- Duplicate `.env.example` file and rename to `.env`
- Populate envs vars in `.env` file
- Run the migrations: `python manage.py migrate`;
- Create a superuser: `python manage.py createsuperuser`;
- Run the server: `python manage.py runserver`.

# Asynchronous task
- Run Redis server
- Run celery `make celery`  to development

## Install git pre-commit hook
Check code syntax and style before commit changes.

After initializing git, add flake8 hook.
```bash
$ python -m flake8 --install-hook git
$ pre-commit install
```

Set flake8 strict parameter to true, this forces all violations to be fixed
before the commit.
```bash
$ git config --bool flake8.strict true
```
