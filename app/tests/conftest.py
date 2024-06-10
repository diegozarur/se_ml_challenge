import pytest
from app import create_app


class TestingConfig:
    TESTING = True
    UPLOAD_FOLDER = "tests/docs"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


@pytest.fixture()
def app():
    app = create_app(TestingConfig)

    # other setup can go here
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
