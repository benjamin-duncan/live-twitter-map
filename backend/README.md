# /backend/
**Django, Django REST Framework, Celery/Celery Beat, Channels, Redis, PostgreSQL, Tweepy & Docker.**

Ideally, the backend is run using *``docker-compose``* in development. Each container uses the same base Docker image.
## Testing

The [pytest](https://pytest.org) framework can be run using manually or as part of CI/CD workflow:

```[sh]
cd backend
pip install requirements-test.txt
pytest
```
Optionally, [coverage](https://github.com/nedbat/coveragepy) can be used to generate a coverage report:
```[sh]
cd backend
pip install requirements-test.txt
coverage run --source . -m pytest
coverage report
```

[Flake8](https://github.com/PyCQA/flake8) and [Black](https://github.com/psf/black) can also be used for linting and code formatting to meet [PEP8](https://www.python.org/dev/peps/pep-0008/) guidelines:
```[sh]
cd backend
black .
flake8 --output-file pep8_report.txt
```

## Additional Files
#### *``check_db.sh``*
During startup, this script ensures the PostgreSQL database is running before fully starting the Django Web App.

#### *``pytest.ini``*
Ensures pytest correctly uses Django's settings when testing. In some cases, separate settings may be used for dev/test/prod (outside of environment variable configuration).

This Django Applications is adapted from https://github.com/gonzalo123/clock

