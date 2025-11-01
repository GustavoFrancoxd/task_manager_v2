from datetime import timedelta
from app.utils.get_ip import get_local_ip, get_public_ip
import os


#ejemplo para crear variable de entorno en windows
#[System.Environment]::SetEnvironmentVariable("SECRET_KEY", "mypasswordortokenorsecret", "User") 

class Config:
    # se le pone modo debug y se le asigna un nombre al servidor, en este caso una direccion ip
    DEBUG = True #desactivar en produccion
    if DEBUG:
        SERVER_NAME = f"{get_local_ip()}:5001" #usar solo en ambiente privado, no de produccion
    else:
        SERVER_NAME = f"{get_public_ip()}:5001" #usar solo al subirlo al servidor

    # clave secreta para encriptar sesiones
    SECRET_KEY = os.environ.get("SECRET_KEY")
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # configuracion de conexion a base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = str(MAIL_USERNAME)


print(Config.SQLALCHEMY_DATABASE_URI)
print(Config.SERVER_NAME)
print(Config.SECRET_KEY)