import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planets import Planet


@pytest.fixture
def app():
    app = create_app({"Testing": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def two_planets(app):
    mercury = Planet(id = 1, name = "Mercury", description = "planet y", number_of_moons = 0)
    venus = Planet(id = 2, name = "Venus", description = "planet x", number_of_moons = 0)

    db.session.add_all([mercury, venus])

    db.session.commit()
