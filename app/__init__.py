from flask import Flask
from app.config import Db_Config
from app.routes import register_blueprints
from flask_bootstrap import Bootstrap
from app.extensions import database

#mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Db_Config)
    bootstrap = Bootstrap(app)
    register_blueprints(app)
    database.init_app(app)
    return app
