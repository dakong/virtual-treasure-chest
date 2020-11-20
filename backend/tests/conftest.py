import pytest
from webtest import TestApp
from config import TestConfig
from app import create_app
from app.database import db as _db


@pytest.fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()
    yield _db
    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()
