from .auth_routes import auth
from .task_routes import task


def register_blueprints(app: object):
    """
    funcion para registrar todos los blueprints en el objeto Flask

    Args:
        app (Flask): Aplicacion flask
    """
    app.register_blueprint(auth)
    app.register_blueprint(task)
