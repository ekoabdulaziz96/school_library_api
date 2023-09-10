# school_api

App scholl API project

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## How to run
1. clone this project, and make sure your current position is in root folder.
2. Activate your python virtual environment, if you use it (develop in python 3.9.17)
3. duplicate `env.example` file, and rename it to `.env` file (please fill your setting/config like DB, redis, etc)
3. install the python requirement `pip install -r requirements/local.txt`
4. migrate the database `python manage.py migrate`
    - if you need dummy data for book, just run `python manage.py loaddata dummy-books.json`
5. create your superuser account `python manage.py createsuperuser`
    - to get role superadmin, you can modify your superuser in django admin `{base_url}/admin` then access user menu
6. run your project `python manage.py runserver`

NB: 
- to read more about the requirement, postman collection, ERD you can find it on `xresources` folder
- for api spec, you can access the swagger (open-api) with superuser credential -->  `{base_url}/api/docs` 
- For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

## Pre-commit manual, to do:
```sh
# in short / summary for automatically format your code
flake8 --config=setup.cfg .
isort .
black --config .\pyproject.toml .

# you can repeat it , and recheck
# more detail in below
```

### Linting check with flake8 [mandatory]:
- run:
    ```sh
    # run flake8 for global/specific target
    flake8 --config=setup.cfg .
    flake8 --config=setup.cfg app_name/sub_folder

    # diff check
    git diff -u | flake8 --config=setup.cfg --diff
    ```
- ignore:
    ```sh
    # add comment in your file/specific line

    # flake8: noqa  --> file

    code = 'your code' # noqa          --> line
    code = 'your code' # noqa: E731    --> line and specific error
    ```

### Fix import sorting with isort [optional]:
- run
    ```sh
    isort .
    isort  app_name/sub_folder
    ```
- ignore
    ```sh
    # add comment in your file/specific line

    # isort: skip_file  --> skip entire file
    # isort: split      --> split

    # isort: off        --> start off
    import not_sorted
    import not_sorted
    import not_sorted
    # isort: on         --> start on
    ```

### Auto Formatter with black [mandatory]:
- run
    ```
    black --config .\pyproject.toml .
    black --config .\pyproject.toml  app_name/sub_folder
    ```
- ignore
    ```sh
    # add comment your specific line

    # fmt: off
    code = 'your code'
    # fmt: on
    ```

## Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```sh
    # run coverate in unittest
    coverage run -m pytest
    coverage run -m pytest path/app

    # make html report
    coverage report
    coverage html

    # open htmlcov/index.html in browser
```

## Running tests with pytest
```sh
    pytest
    pytest path/app

    # ex: specific test-case
    # pytest path/module::class-name::func-name
    pytest qazwa/users/tests/api/test_user_register.py::UserRegisterVerifyOtpTest::test_success_verify_otp
```


## Celery

Please note: To set broker in .env file. and for Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process.

```bash
cd school_api
celery -A config.celery_app worker -l info   # a celery worker:
celery -A config.celery_app beat     # run periodic task (can be standalone process)
```
