from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generar_token_confirmacion(email):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps(email, salt="confirmar-correo")


def verificar_token_confirmacion(token, max_age=3600):  # 1 hora por defecto
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt="confirmar-correo", max_age=max_age)
    except Exception:
        return None
    return email
