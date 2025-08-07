from flask import render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import Usuario
from app.extensions import database, mail
from flask_mail import Message  # type: ignore
from datetime import datetime, timedelta
import secrets, re
from app.utils.token import generar_token_confirmacion, verificar_token_confirmacion
from app.forms.auth_forms import (
    LoginForm,
    SigninForm,
    PasswordResetRequestForm,
    PasswordResetForm,
)


def login_controller():
    if "email" not in session:
        login_form = LoginForm()

        context = {"login_form": login_form}

        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = Usuario.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                if not user.confirmado:
                    print("Tu correo aún no ha sido confirmado.")
                    return redirect(url_for("auth.login"))
                else:
                    session["email"] = email
                    return redirect(url_for("task.dashboard"))
        return render_template("login.html", **context)
    else:
        return redirect(url_for("task.dashboard"))


def logout_controller():
    session.clear()  # Elimina todos los datos de la sesión
    return redirect(url_for("auth.login"))  # Redirige al login


def signin_controller():
    signin_form = SigninForm()

    context = {"signin_form": signin_form}

    if signin_form.validate_on_submit():
        email = signin_form.email.data
        password = signin_form.password.data

        try:
            if Usuario.query.filter_by(email=email).first():
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

            nuevo_usuario = Usuario(email=email, password=hashed_password)
            token = generar_token_confirmacion(nuevo_usuario.email)
            nuevo_usuario.token = token
            nuevo_usuario.token_expira = datetime.utcnow() + timedelta(hours=1)
            database.session.add(nuevo_usuario)
            database.session.commit()

            confirm_url = url_for("auth.confirm_email", token=token, _external=True)

            msg = Message("Confirma tu cuenta", recipients=[nuevo_usuario.email])
            msg.body = f"Por favor haz clic en el siguiente enlace para confirmar tu cuenta:\n{confirm_url}"
            mail.send(msg)

            print("Se envió un correo de confirmación.")

            return redirect(url_for("auth.login"))  # Redirige al login
        except ValueError as ve:
            print(f"Error de validación: {ve}")
        # except pymysql.err.IntegrityError as e:
        except IntegrityError as e:  # type: ignore
            if "1062" in str(e):
                # flash("Ese nombre de usuario ya está en uso. Intenta con otro.", "danger")
                print("Ese nombre de usuario ya está en uso. Intenta con otro.")
            else:
                # flash("Ocurrió un error inesperado.", "danger")
                print("Ocurrió un error inesperado.")
        except Exception as e:
            print(f"Error inesperado: {e}")

    return render_template("signin.html", **context)


def confirm_email_controller(token):
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


def reset_request_controller():
    form = PasswordResetRequestForm()

    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
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
                recipients=[user.email],
            )
            msg.body = f"Hola, haz clic en el siguiente enlace para cambiar tu contraseña:\n{reset_link}"
            mail.send(msg)
            print("Se envió un enlace a tu correo.")
            # flash("Se envió un enlace a tu correo.", "info")
        else:
            print("Usuario no encontrado.")
            # flash("Usuario no encontrado.", "warning")
        return redirect(url_for("auth.login"))

    return render_template("reset_request.html", form=form)


def reset_token_controller(token):
    user = Usuario.query.filter_by(token=token).first()
    print(f"nombre de usuario: {user.email}")
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
