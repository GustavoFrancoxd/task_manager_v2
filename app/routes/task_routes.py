from flask import Blueprint, render_template, redirect, session, url_for
from app.forms.task_forms import NotaForm
from app.models.models import Usuario, Tarea, Crea
from app.extensions import database

task = Blueprint('task', __name__)

@task.route('/dashboard')
def dashboard():
    #from app import mysql
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    #cursor = mysql.connection.cursor()
    # Obtener el ID del usuario con su username de la sesión
    #cursor.execute("SELECT id_usuario FROM usuario WHERE username = %s", (session['username'],))
    #usuario = cursor.fetchone()
    usuario = Usuario.query.filter_by(username=session['username']).first()

    if not usuario:
        return redirect(url_for('auth.login'))  # Seguridad por si algo falla

    #id_usuario = usuario['id_usuario']
    id_usuario = usuario.id_usuario

    # Obtener tareas creadas por el usuario con fecha y estado
    #query = """
    #    SELECT t.id_tarea, t.contenido, t.completado, c.fecha_creacion
    #    FROM tarea t
    #    JOIN crea c ON t.id_tarea = c.fk_tarea
    #    WHERE c.fk_usuario = %s
    #    ORDER BY c.fecha_creacion DESC
    #"""
    #cursor.execute(query, (id_usuario,))
    #tareas = cursor.fetchall()
    #cursor.close()
    
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
    #from app import mysql
    #cur = mysql.connection.cursor()
    # Alterna el estado: si está en 1, lo cambia a 0 y viceversa
    #cur.execute("""
    #    UPDATE tarea 
    #    SET completado = NOT completado 
    #    WHERE id_tarea = %s
    #""", (nota_id,))
    #mysql.connection.commit()
    #cur.close()
    tarea = Tarea.query.get(nota_id)
    if tarea:
        tarea.completado = not tarea.completado  # invierte el valor actual (True ↔ False)
        database.session.commit()
    return redirect(url_for('task.dashboard'))

@task.route('/crear', methods=['GET', 'POST'])
def crear_nota():
    #from app import mysql
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    form = NotaForm()

    if form.validate_on_submit():
        contenido = form.contenido.data

        #cur = mysql.connection.cursor()

        # Obtener ID del usuario
        #cur.execute("SELECT id_usuario FROM usuario WHERE username = %s", (session['username'],))
        #usuario = cur.fetchone()
        usuario = Usuario.query.filter_by(username=session['username']).first()
        if not usuario:
            #flash('Usuario no encontrado.')
            return redirect(url_for('auth.login'))

        id_usuario = usuario['id_usuario']

        # Insertar nueva tarea
        #cur.execute("INSERT INTO tarea (contenido, completado) VALUES (%s, %s)", (contenido, 0))
        #id_tarea = cur.lastrowid
        nueva_tarea = Tarea(contenido=contenido, completado=False)
        database.session.add(nueva_tarea)
        database.session.commit()
        id_tarea = nueva_tarea.id_tarea

        # Insertar en la tabla crea
        #cur.execute("INSERT INTO crea (fk_usuario, fk_tarea, fecha_creacion) VALUES (%s, %s, NOW())", (id_usuario, id_tarea))
        #mysql.connection.commit()
        #cur.close()
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
