from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.forms.auth_forms import (
    LoginForm,
    SigninForm,
    PasswordResetRequestForm,
    PasswordResetForm,
)
from werkzeug.security import generate_password_hash, check_password_hash
import re  # libreria de expresiones regulares excelentes para validaciones
from sqlalchemy.exc import IntegrityError
from app.models.models import Usuario
from app.extensions import database
from app.extensions import mail
from flask_mail import Message
from datetime import datetime, timedelta
import secrets
from app.utils.token import generar_token_confirmacion, verificar_token_confirmacion

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if "username" not in session:
        login_form = LoginForm()

        context = {"login_form": login_form}

        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            user = Usuario.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                if not user.confirmado:
                    print("Tu correo aún no ha sido confirmado.")
                    return redirect(url_for("auth.login"))
                else:
                    session["username"] = username
                    return redirect(url_for("task.dashboard"))
        return render_template("login.html", **context)
    else:
        return redirect(url_for("task.dashboard"))


@auth.route("/logout")
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    return redirect(url_for("auth.login"))  # Redirige al login


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    signin_form = SigninForm()

    context = {"signin_form": signin_form}

    if signin_form.validate_on_submit():
        username = signin_form.username.data
        password = signin_form.password.data

        try:
            if Usuario.query.filter_by(username=username).first():
                raise ValueError("Este correo ya está registrado.")

            if (
                len(password) < 7
                or not re.search(r"[A-Z]", password)
                or not re.search(r"\d", password)
                or not re.search(r'[!@#$%^&*(),.?":{}|<>_-]', password)
            ):
                raise ValueError(
                    "La contraseña debe tener mínimo 7 caracteres, incluir una mayúscula, un número y un símbolo."
                )

            hashed_password = generate_password_hash(password)
            confirm_password = signin_form.confirm_password.data

            if password != confirm_password:
                raise ValueError("Las contraseñas no coinciden.")

            nuevo_usuario = Usuario(username=username, password=hashed_password)
            token = generar_token_confirmacion(nuevo_usuario.username)
            nuevo_usuario.token = token
            nuevo_usuario.token_expira = datetime.utcnow() + timedelta(hours=1)
            database.session.add(nuevo_usuario)
            database.session.commit()

            confirm_url = url_for("auth.confirm_email", token=token, _external=True)

            msg = Message("Confirma tu cuenta", recipients=[nuevo_usuario.username])
            msg.body = f"Por favor haz clic en el siguiente enlace para confirmar tu cuenta:\n{confirm_url}"
            mail.send(msg)

            print("Se envió un correo de confirmación.")

            return redirect(url_for("auth.login"))  # Redirige al login
        except ValueError as ve:
            print(f"Error de validación: {ve}")
        # except pymysql.err.IntegrityError as e:
        except IntegrityError as e:
            if "1062" in str(e):
                # flash("Ese nombre de usuario ya está en uso. Intenta con otro.", "danger")
                print("Ese nombre de usuario ya está en uso. Intenta con otro.")
            else:
                # flash("Ocurrió un error inesperado.", "danger")
                print("Ocurrió un error inesperado.")
        except Exception as e:
            print(f"Error inesperado: {e}")

    return render_template("signin.html", **context)


@auth.route("/confirm/<token>")
def confirm_email(token):
    user = Usuario.query.filter_by(token=token).first()

    if not user:
        print("Token inválido.")
        return redirect(url_for("auth.login"))

    if not user.token_expira or datetime.utcnow() > user.token_expira:
        print("Token expirado.")
        return redirect(url_for("auth.login"))

    user.confirmado = True
    user.token = None
    user.token_expira = None
    database.session.commit()

    print("Correo confirmado con éxito.")
    return redirect(url_for("auth.login"))


@auth.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    form = PasswordResetRequestForm()

    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user:
            token = secrets.token_urlsafe(32)
            user.token = token
            user.token_expira = datetime.utcnow() + timedelta(
                minutes=30
            )  # Expira en 30 minutos
            reset_link = url_for("auth.reset_token", token=token, _external=True)
            user.token = token
            database.session.commit()

            # Enviar correo
            msg = Message(
                "Recuperar contraseña",
                sender="gustavofranco2530@gmail.com",
                recipients=[user.username],
            )  # suponiendo que el username es el correo
            msg.body = f"Hola, haz clic en el siguiente enlace para cambiar tu contraseña:\n{reset_link}"
            mail.send(msg)
            print("Se envió un enlace a tu correo.")
            # flash("Se envió un enlace a tu correo.", "info")
        else:
            print("Usuario no encontrado.")
            # flash("Usuario no encontrado.", "warning")
        return redirect(url_for("auth.login"))

    return render_template("reset_request.html", form=form)


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    user = Usuario.query.filter_by(token=token).first()
    print(f"nombre de usuario: {user.username}")
    if not user or not user.token_expira or datetime.utcnow() > user.token_expira:
        print("Token inválido o expirado.")
        return redirect(url_for("auth.reset_request"))

    form = PasswordResetForm()
    if form.validate_on_submit():
        password = form.password.data
        confirm_password = form.confirm_password.data
        try:
            if password != confirm_password:
                print("Las contraseñas no coinciden.")
                # flash("Las contraseñas no coinciden.", "danger")
            elif (
                len(password) < 7
                or not re.search(r"[A-Z]", password)
                or not re.search(r"\d", password)
                or not re.search(r'[!@#$%^&*(),.?":{}|<>_-]', password)
            ):
                raise ValueError(
                    "La contraseña debe tener mínimo 7 caracteres, incluir una mayúscula, un número y un símbolo."
                )
            else:
                user.password = generate_password_hash(password)
                user.token = None
                database.session.commit()
                print("Contraseña actualizada con éxito.")
                # flash("Contraseña actualizada con éxito.", "success")
                return redirect(url_for("auth.login"))
        except ValueError as ve:
            print(f"Error de validación: {ve}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    return render_template("reset_with_token.html", form=form)
