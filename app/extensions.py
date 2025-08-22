from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

"""
    este archivo contiene la conexion a la base de datos,
    y tambien la conexion al correo. se guardan como extensiones,
    para evitar error con la importacion redundante.
"""

database = SQLAlchemy()
mail = Mail()
