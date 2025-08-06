from flask import Flask
from app.config import Config
from app.routes import register_blueprints
from flask_bootstrap import Bootstrap
from app.extensions import database, mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Bootstrap(app)
    database.init_app(app)
    mail.init_app(app)
    register_blueprints(app)

    return app
