from flask import render_template, redirect, session, url_for
from app.forms.task_forms import NotaForm
from app.forms.modify_form import ModifyForm
from app.models.models import Usuario, Tarea, Crea, HistorialTarea
from app.extensions import database


def dashboard_controller():
    if "email" not in session:
        return redirect(url_for("auth.login"))

    usuario = Usuario.query.filter_by(email=session["email"]).first()

    if not usuario:
        return redirect(url_for("auth.login"))

    id_usuario = usuario.id_usuario

    tareas = (
        database.session.query(
            Tarea.id_tarea,
            Tarea.contenido,
            Tarea.completado,
            Tarea.activo,
            Crea.fecha_creacion,
        )
        .join(Crea, Tarea.id_tarea == Crea.fk_tarea)
        .filter(Crea.fk_usuario == id_usuario)
        .order_by(Crea.fecha_creacion.desc())
        .all()
    )

    context = {"notas": tareas, "email": session["email"]}

    return render_template("dashboard.html", **context)


def cambiar_estatus_controller(nota_id):
    if "email" not in session:
        return redirect(url_for("auth.login"))

    tarea = Tarea.query.get(nota_id)
    if tarea:
        tarea.completado = (
            not tarea.completado
        )  # invierte el valor actual (True ↔ False)
        historial = HistorialTarea(
            fk_tarea=tarea.id_tarea,
            contenido=tarea.contenido,
            completado=tarea.completado,
            activo=tarea.activo,
        )
        database.session.add(historial)

        database.session.commit()
    return redirect(url_for("task.dashboard"))


def crear_nota_controller():
    if "email" not in session:
        return redirect(url_for("auth.login"))

    form = NotaForm()

    if form.validate_on_submit():
        contenido = form.contenido.data

        usuario = Usuario.query.filter_by(email=session["email"]).first()
        if not usuario:
            # flash('Usuario no encontrado.')
            return redirect(url_for("auth.login"))

        id_usuario = usuario.id_usuario

        # Insertar nueva tarea
        nueva_tarea = Tarea(contenido=contenido, completado=False)
        database.session.add(nueva_tarea)
        database.session.commit()

        # Insertar en la tabla crea
        nueva_relacion = Crea(fk_usuario=id_usuario, fk_tarea=nueva_tarea.id_tarea)
        database.session.add(nueva_relacion)
        database.session.commit()

        historial = HistorialTarea(
            fk_tarea=nueva_tarea.id_tarea,
            contenido=nueva_tarea.contenido,
            completado=nueva_tarea.completado,
            activo=nueva_tarea.activo,
        )
        database.session.add(historial)

        database.session.commit()

        # flash('Nota creada exitosamente.', 'success')
        return redirect(url_for("task.dashboard"))

    context = {"form": form, "email": session["email"]}

    return render_template("createnote.html", **context)


def eliminar_nota_controller(nota_id):
    if "email" not in session:
        return redirect(url_for("auth.login"))

    tarea = Tarea.query.get_or_404(nota_id)
    tarea.activo = False
    historial = HistorialTarea(
        fk_tarea=tarea.id_tarea,
        contenido=tarea.contenido,
        completado=tarea.completado,
        activo=tarea.activo,
    )
    database.session.add(historial)
    database.session.commit()
    return redirect(url_for("task.dashboard"))


def editar_nota_controller(nota_id):
    if "email" not in session:
        return redirect(url_for("auth.login"))

    tarea = Tarea.query.get_or_404(nota_id)
    form = ModifyForm(obj=tarea)  # precarga valores

    if form.validate_on_submit():
        # Modificar los campos actuales
        tarea.contenido = form.contenido.data
        tarea.completado = form.completado.data
        database.session.commit()

        # Guardar el historial despues de modificar
        historial = HistorialTarea(
            fk_tarea=tarea.id_tarea,
            contenido=tarea.contenido,
            completado=tarea.completado,
            activo=tarea.activo,
        )
        database.session.add(historial)
        database.session.commit()

        return redirect(url_for("task.dashboard"))

    context = {"form": form, "email": session["email"], "nota_id": nota_id}
    return render_template("editnote.html", **context)
