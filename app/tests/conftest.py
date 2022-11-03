from app.models.book import Book
import pytest
from app import create_app
from app import db
from flask.signals import request_finished

@pytest.fixture
def app():
    app = create_app({"TESTING": True}) # if True, swaps to testing db

    # this fx makes sure it clears out the temporary data with every request
    # helps us make sure our tests are accurately checking the data
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        # generates a clean start, empty models and tables for us to test on
        db.create_all()
        # yield tells our fixture to return an instance of our app_context and send it to our test
        yield app

    with app.app_context():
        # this clears out any data that was created while testing
        db.drop_all()


@pytest.fixture
# this fx will take in the app fixture
def client(app): # this fx will simulate our client, to make requests through these test routes
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book",
                      description="watr 4evr")
    mountain_book = Book(title="Mountain Book",
                         description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit()