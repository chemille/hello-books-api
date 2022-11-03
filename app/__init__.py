from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate() 
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # DB Config
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if not test_config: # if flag variable is None or False, it will connect to our development db
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'SQLALCHEMY_DATABASE_URI')
    # else if True, it will be part of our test db so that we can start creating tests to check routes & how to store this test info for those tests
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'SQLALCHEMY_TEST_DATABASE_URI')
    
    # Register Blueprints here    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models here    
    from app.models.book import Book
    
    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app