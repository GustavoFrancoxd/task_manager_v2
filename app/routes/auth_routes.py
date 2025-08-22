from flask import Blueprint
from app.controllers.auth_controller import (
    login_controller,
    logout_controller,
    signin_controller,
    confirm_email_controller,
    reset_request_controller,
    reset_token_controller,
)

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    #lleva al controlador encargado de mostrar el template y procesar el inicio de sesion
    return login_controller()


@auth.route("/logout")
def logout():
    #controlador encargado de terminar la sesion del usuario
    return logout_controller()


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    #controlador encargado de mostrar formulario, registrar usuarios nuevos y mandar correo de confirmacion
    return signin_controller()


@auth.route("/confirm/<token>")
def confirm_email(token):
    #controlador encargado de validar token de usuarios registrados
    return confirm_email_controller(token)


@auth.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    #controlador encargado de enviar un token para resetear password
    return reset_request_controller()


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    #controlador encargado de validar token de reseteo de password
    return reset_token_controller(token)
