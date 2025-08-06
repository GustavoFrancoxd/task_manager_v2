from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class NotaForm(FlaskForm):
    contenido = TextAreaField(
        "Contenido",
        validators=[
            DataRequired(message="El contenido es obligatorio."),
            Length(min=5, max=1000, message="Debe tener entre 5 y 1000 caracteres."),
        ],
    )
    submit = SubmitField("Guardar Nota")
