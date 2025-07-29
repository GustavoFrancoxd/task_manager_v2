from datetime import datetime
from app.extensions import database 

class Usuario(database.Model):
    __tablename__ = 'usuario'
    id_usuario = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    crea = database.relationship('Crea', backref='usuario', lazy=True)

class Tarea(database.Model):
    __tablename__ = 'tarea'
    id_tarea = database.Column(database.Integer, primary_key=True)
    contenido = database.Column(database.String(255), nullable=False)
    completado = database.Column(database.Boolean, default=False)
    crea = database.relationship('Crea', backref='tarea', lazy=True)

class Crea(database.Model):
    __tablename__ = 'crea'
    id = database.Column(database.Integer, primary_key=True)
    fk_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id_usuario'), nullable=False)
    fk_tarea = database.Column(database.Integer, database.ForeignKey('tarea.id_tarea'), nullable=False)
    fecha_creacion = database.Column(database.DateTime, default=datetime.utcnow)