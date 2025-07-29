from .auth_routes import auth
from .task_routes import task

def register_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(task)