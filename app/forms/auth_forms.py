from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Nombre del usuario', validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')
    
class SigninForm(FlaskForm):
    username = StringField('Nombre del usuario', validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    confirm_password =  PasswordField('Confirmar password', validators=[DataRequired()])
    submit = SubmitField('Enviar')