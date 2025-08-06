from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class ModifyForm(FlaskForm):
    contenido = TextAreaField(
        "Contenido",
        validators=[
            DataRequired(message="El contenido es obligatorio."),
            Length(min=5, max=1000, message="Debe tener entre 5 y 1000 caracteres."),
        ],
    )
    completado = BooleanField("¿Completado?")
    submit = SubmitField("Guardar Nota")
