from flask import Blueprint, render_template, redirect, session, url_for
from app.forms.task_forms import NotaForm
from app.forms.modify_form import ModifyForm
from app.models.models import Usuario, Tarea, Crea, HistorialTarea
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
        database.session.query(Tarea.id_tarea, Tarea.contenido, Tarea.completado, Tarea.activo, Crea.fecha_creacion)
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
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    tarea = Tarea.query.get(nota_id)
    if tarea:
        tarea.completado = not tarea.completado  # invierte el valor actual (True ↔ False)
        historial = HistorialTarea(
            fk_tarea=tarea.id_tarea,
            contenido=tarea.contenido,
            completado=tarea.completado,
            activo= tarea.activo
        )
        database.session.add(historial)
        
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

        # Insertar en la tabla crea
        nueva_relacion = Crea(fk_usuario=id_usuario, fk_tarea=nueva_tarea.id_tarea)
        database.session.add(nueva_relacion)
        database.session.commit()
        
        historial = HistorialTarea(
            fk_tarea=nueva_tarea.id_tarea,
            contenido=nueva_tarea.contenido,
            completado=nueva_tarea.completado,
            activo= nueva_tarea.activo
        )
        database.session.add(historial)
        
        database.session.commit()

        #flash('Nota creada exitosamente.', 'success')
        return redirect(url_for('task.dashboard'))

    context = {
        'form': form,
        'username': session['username']
    }

    return render_template('createnote.html', **context)

@task.route('/eliminar/<int:nota_id>', methods=['POST'])
def eliminar_nota(nota_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    tarea = Tarea.query.get_or_404(nota_id)
    tarea.activo = False
    historial = HistorialTarea(
        fk_tarea=tarea.id_tarea,
        contenido=tarea.contenido,
        completado=tarea.completado,
        activo= tarea.activo
    )
    database.session.add(historial)
    database.session.commit()
    return redirect(url_for('task.dashboard'))


@task.route('/editar/<int:nota_id>', methods=['GET', 'POST'])
def editar_nota(nota_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    tarea = Tarea.query.get_or_404(nota_id)
    form = ModifyForm(obj=tarea)  # precarga valores

    if form.validate_on_submit():
        # Modificar los campos actuales
        tarea.contenido = form.contenido.data
        tarea.completado = form.completado.data
        database.session.commit()
        
        #Guardar el historial despues de modificar
        historial = HistorialTarea(
            fk_tarea=tarea.id_tarea,
            contenido=tarea.contenido,
            completado=tarea.completado,
            activo= tarea.activo
        )
        database.session.add(historial)
        database.session.commit()
        
        return redirect(url_for('task.dashboard'))

    context = {
        'form': form,
        'username': session['username'],
        'nota_id': nota_id
    }
    return render_template('editnote.html', **context)
