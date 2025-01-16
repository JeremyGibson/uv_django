# {{ cookiecutter.project_name }}


## ✏️ **Develop**
To begin you should have the following applications installed on your local development system:

- Python >= {{ cookiecutter.python_version }}
- bun
- uv
- Postgres >= {{ cookiecutter.postgres_version }}
- git >= 2.26

### 💪 **Setup Manually**

**1. Get the project**

First clone the repository from Github and switch to the new directory:

```linux
    $ git clone git@github.com:caktus/{{ cookiecutter.project_app }}.git
    $ cd {{ cookiecutter.project_app }}
```

**2. Set up virtual environment**

Next, set up your virtual environment with python3. For example, ``{{ cookiecutter.project_app }}``.

You will note the distinct lack of opinion on how you should manage your virtual environment. This is by design.


**3. Install dependencies**

``nvm`` is preferred for managing Node versions and ``.nvmrc`` contains the
specific Node version for this project. To install the correct (and latest)
Node version run:

```sh
    ({{ cookiecutter.project_app }})$ nvm install
```

Now install the project Node packages with ``npm``:

```sh
    ({{ cookiecutter.project_app }})$ npm install
```

Install Python dependencies with:

```linux
    ({{ cookiecutter.project_app }})$ make setup
```

{% if cookiecutter.include_accessibility_tests == 'yes' %}
This project has been set up to run automated accessibility tests,
which require [geckodriver](https://github.com/mozilla/geckodriver/).

To install on Linux:

```
$ curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz > geckodriver.tar.gz
$ tar -zxvf geckodriver.tar.gz
$ sudo mv geckodriver /usr/local/bin
```

To install on Mac:

```
$ brew install geckodriver
```

{% if cookiecutter.testing_type == 'pytest' %}
Note that accessibility tests run before migration checks, so any test errors in the accessibility tests will be output before any of the migration information. You may need to scroll up further than you expect in order to see the accessibility test errors, beginning with ``Accessibility violations:``
{% endif %}
{% endif %}

NOTE: This project uses ``pip-tools``. If the dependency `.txt` files need to be
updated:

```sh
    ({{ cookiecutter.project_app }})$ make update_requirements setup
```

NOTE 2: During a development cycle if a developer needs to add subtract or modify the requirements of the project, the
workflow is to:

1) Make the change in the ``*.in`` requirement file
2) run ``make update_requirements``
3) commit both ``*.in`` file(s) and the ``*.txt`` file(s) generated


**4. Pre-commit**

pre-commit is used to enforce a variety of community standards. CI runs it,
so it's useful to setup the pre-commit hook to catch any issues before pushing
to GitHub and reset your pre-commit cache to make sure that you're starting fresh.

To install, run:

```linux
    ({{ cookiecutter.project_app }})$ pre-commit clean
    ({{ cookiecutter.project_app }})$ pre-commit install
```


**5. Set up local env variables**

Next, we'll set up our local environment variables. We use
[django-dotenv](https://github.com/jpadilla/django-dotenv) to automatically read
environment variables located in a file named `.env` in the top level directory of the
project (but you may use any other way of setting environment variables, like direnv or
manually setting them). The only variable we need to start is `DJANGO_SETTINGS_MODULE`:

```linux
    ({{ cookiecutter.project_app }})$ cp {{ cookiecutter.project_app }}/settings/local.example.py {{ cookiecutter.project_app }}/settings/local.py
    ({{ cookiecutter.project_app }})$ echo "DJANGO_SETTINGS_MODULE={{ cookiecutter.project_app }}.settings.local" > .env
```


**6. Database**

The setup for local development assumes that you will be working with dockerized
services.

First add the following line to your `.env` file:

```sh
({{ cookiecutter.project_app }})$ echo "DATABASE_URL=postgres://postgres@127.0.0.1:{{ cookiecutter.postgres_port }}/{{ cookiecutter.project_app }}" >> .env
```

The `docker-compose.yml` sets up environment variables in a file, ``.postgres``.
To use the Docker setup, add these lines to that file:

```sh
    POSTGRES_DB={{ cookiecutter.project_app }}
    POSTGRES_HOST_AUTH_METHOD=trust
```

If you want to connect to the database from your host machine, export the
following shell environment variables:

```sh
    export PGHOST=127.0.0.1
    export PGPORT={{ cookiecutter.postgres_port }}
    export PGUSER=postgres
    export PGDATABASE={{ cookiecutter.project_app }}
```


**7. Migrate and create a superuser**

```linux
    ({{ cookiecutter.project_app }})$ docker-compose up -d
    ({{ cookiecutter.project_app }})$ python manage.py migrate
    ({{ cookiecutter.project_app }})$ python manage.py createsuperuser
```

**8. Run the server**

```linux
    ({{ cookiecutter.project_app }})$ docker-compose up -d
    ({{ cookiecutter.project_app }})$ make run-dev
```

After initial setup the development server should be run using ``make run-dev`` this will remove any deployment containers hanging around and setup using local sources and database.


**9. Access the server**

The Django admin is at `/admin` and the Wagtail admin is at `/cms`.


**10. Run tests**

{{ cookiecutter.project_app }} uses pytest as a test runner.


```sh
    ({{ cookiecutter.project_app }})$ make run-tests
```