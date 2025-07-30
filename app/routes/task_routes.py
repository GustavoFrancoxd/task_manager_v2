from flask import Blueprint, render_template, redirect, session, url_for
from app.forms.task_forms import NotaForm
from app.models.models import Usuario, Tarea, Crea
from app.extensions import database

task = Blueprint('task', __name__)

@task.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    usuario = Usuario.query.filter_by(username=session['username']).first()

    if not usuario:
        return redirect(url_for('auth.login'))

    id_usuario = usuario.id_usuario
    
    tareas = (
        database.session.query(Tarea.id_tarea, Tarea.contenido, Tarea.completado, Crea.fecha_creacion)
        .join(Crea, Tarea.id_tarea == Crea.fk_tarea)
        .filter(Crea.fk_usuario == id_usuario)
        .order_by(Crea.fecha_creacion.desc())
        .all()
    )

    context = {
        "notas": tareas,
        "username": session['username']
    }

    return render_template('dashboard.html', **context)


@task.route('/cambiar_estatus/<int:nota_id>', methods=['POST'])
def cambiar_estatus(nota_id):
    tarea = Tarea.query.get(nota_id)
    if tarea:
        tarea.completado = not tarea.completado  # invierte el valor actual (True ↔ False)
        database.session.commit()
    return redirect(url_for('task.dashboard'))

@task.route('/crear', methods=['GET', 'POST'])
def crear_nota():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    form = NotaForm()

    if form.validate_on_submit():
        contenido = form.contenido.data

        usuario = Usuario.query.filter_by(username=session['username']).first()
        if not usuario:
            #flash('Usuario no encontrado.')
            return redirect(url_for('auth.login'))

        id_usuario = usuario.id_usuario

        # Insertar nueva tarea
        nueva_tarea = Tarea(contenido=contenido, completado=False)
        database.session.add(nueva_tarea)
        database.session.commit()
        id_tarea = nueva_tarea.id_tarea

        # Insertar en la tabla crea
        nueva_relacion = Crea(fk_usuario=id_usuario, fk_tarea=id_tarea)
        database.session.add(nueva_relacion)
        database.session.commit()

        #flash('Nota creada exitosamente.', 'success')
        return redirect(url_for('task.dashboard'))

    context = {
        'form': form,
        'username': session['username']
    }

    return render_template('createnote.html', **context)
