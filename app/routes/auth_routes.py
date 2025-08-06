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
    return login_controller()


@auth.route("/logout")
def logout():
    return logout_controller()


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    return signin_controller()


@auth.route("/confirm/<token>")
def confirm_email(token):
    return confirm_email_controller(token)


@auth.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    return reset_request_controller()


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    return reset_token_controller(token)
