from datetime import timedelta


class Config:
    # se le asigna un nombre al servidor que por defecto es "localhost"
    SERVER_NAME = "192.168.4.45:5001"
    DEBUG = True

    # clave secreta para encriptar sesiones
    SECRET_KEY = "CLAVE SECRETA"
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
