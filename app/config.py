from datetime import timedelta


class Config:
    SERVER_NAME = "192.168.4.35:5001"
    SECRET_KEY = "CLAVE SECRETA"
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # configuracion de conexion a base de datos
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Gfl_25030@localhost:3307/bd_notas"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "gustavofranco2530@gmail.com"
    MAIL_PASSWORD = "sqhvhzwpgjiendqm"
    MAIL_DEFAULT_SENDER = "gustavofranco2530@gmail.com"
