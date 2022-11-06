from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, StringField
from wtforms.validators import InputRequired
from wtforms.widgets import SubmitInput


class ResetInput(SubmitInput):
    input_type = "reset"


class ResetField(SubmitField):
    widget = ResetInput()


class ChangeDataForm(FlaskForm):
    email = EmailField('Почта', render_kw={'readonly': ''})
    name = StringField('Имя', [InputRequired('Это поле обязательно')], id='input_name')
    reset = ResetField('Сбросить изменения')
    submit = SubmitField('Сохранить изменения', id='change_personal')
