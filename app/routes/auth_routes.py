from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.forms.auth_forms import LoginForm, SigninForm
from werkzeug.security import generate_password_hash, check_password_hash
import re #libreria de expresiones regulares excelentes para validaciones
from sqlalchemy.exc import IntegrityError
from app.models.models import Usuario
from app.extensions import database

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if 'username' not in session:
        login_form = LoginForm()
        
        context = {
            'login_form':login_form
        }
        
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            user = Usuario.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['username'] = username
                return redirect(url_for('task.dashboard'))
                                
        return render_template('login.html', **context)
    else:
        return redirect(url_for('task.dashboard'))
    
    
@auth.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    return redirect(url_for('auth.login'))  # Redirige al login
    

@auth.route('/signin', methods=['GET','POST'])
def signin():
    signin_form = SigninForm()
    
    context = {
        'signin_form':signin_form
    }
    
    if signin_form.validate_on_submit():
        username = signin_form.username.data
        password = signin_form.password.data
        
        try:
            if (len(password) < 7 or not re.search(r'[A-Z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>_-]', password)):
                raise ValueError("La contraseña debe tener mínimo 7 caracteres, incluir una mayúscula, un número y un símbolo.")
            
            hashed_password = generate_password_hash(password)
            confirm_password = signin_form.confirm_password.data
            
            if password != confirm_password:
                raise ValueError("Las contraseñas no coinciden.")
            
            nuevo_usuario = Usuario(username=username, password=hashed_password)
            database.session.add(nuevo_usuario)
            database.session.commit()
            return redirect(url_for('auth.login'))  # Redirige al login
        except ValueError as ve:
            print(f"Error de validación: {ve}")
        #except pymysql.err.IntegrityError as e:
        except IntegrityError as e:
            if "1062" in str(e):
                #flash("Ese nombre de usuario ya está en uso. Intenta con otro.", "danger")
                print("Ese nombre de usuario ya está en uso. Intenta con otro.")
            else:
                #flash("Ocurrió un error inesperado.", "danger")
                print("Ocurrió un error inesperado.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    return render_template('signin.html', **context)
    
    