from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
import re


# Validación personalizada de contraseña
def validar_password_segura(form, field):
    password = field.data
    if len(password) < 7:
        raise ValidationError("La contraseña debe tener al menos 7 caracteres.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Debe contener al menos una letra mayúscula.")
    if not re.search(r"\d", password):
        raise ValidationError("Debe contener al menos un número.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-]', password):
        raise ValidationError("Debe contener al menos un símbolo especial.")


class LoginForm(FlaskForm):
    email = StringField("Nombre del usuario", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class SigninForm(FlaskForm):
    email = StringField(
        "email electrónico",
        validators=[
            DataRequired(),
            Email(message="Ingresa un correo electrónico válido"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), validar_password_segura]
    )
    confirm_password = PasswordField(
        "Confirmar password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas no coinciden"),
        ],
    )
    submit = SubmitField("Enviar")


class PasswordResetRequestForm(FlaskForm):
    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(),
            Email(message="Ingresa un correo electrónico válido"),
        ],
    )
    submit = SubmitField("Enviar enlace de recuperación")


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "Nueva contraseña", validators=[DataRequired(), validar_password_segura]
    )
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas no coinciden"),
        ],
    )
    submit = SubmitField("Enviar")
