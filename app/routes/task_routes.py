from flask import Blueprint
from app.controllers.task_controller import (
    dashboard_controller,
    cambiar_estatus_controller,
    crear_nota_controller,
    editar_nota_controller,
    eliminar_nota_controller,
)


task = Blueprint("task", __name__)


@task.route("/dashboard")
def dashboard():
    #controlador encargado de mostrar el dashboard del programa cuando inicie el usuario
    return dashboard_controller()


@task.route("/cambiar_estatus/<int:nota_id>", methods=["POST"])
def cambiar_estatus(nota_id):
    #controlador para cambiar estatus de una nota de un usuario
    return cambiar_estatus_controller(nota_id)


@task.route("/crear", methods=["GET", "POST"])
def crear_nota():
    #controlador para mostrar formulario y crear nota de un usuario
    return crear_nota_controller()


@task.route("/eliminar/<int:nota_id>", methods=["POST"])
def eliminar_nota(nota_id):
    #controlador para eliminar una nota de un usuario
    return eliminar_nota_controller(nota_id)


@task.route("/editar/<int:nota_id>", methods=["GET", "POST"])
def editar_nota(nota_id):
    #controlador para mostrar formulario de editar nota y guardar cambios
    return editar_nota_controller(nota_id)
