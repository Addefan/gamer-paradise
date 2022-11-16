from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, TextAreaField, DecimalField, DateField, IntegerField,
                     BooleanField, SubmitField)
from wtforms.validators import InputRequired, Length, NumberRange, Regexp


class GameForm(FlaskForm):
    title = StringField('Название игры', [InputRequired('Это поле обязательно'),
                                          Length(max=255, message='Название игры должно быть не '
                                                                  'длиннее 255 символов')])
    description = TextAreaField('Описание игры')
    price = DecimalField('Цена игры', [NumberRange(0, message='Цена должна быть неотрицательной')],
                         places=2, default=0)
    photo = FileField('Превью игры', [FileAllowed(['png', 'jpg'],
                                                  'Загружаемый файл должен быть изображением в'
                                                  'формате .png или .jpg')])
    platform = StringField('Платформа', [InputRequired('Это поле обязательно'),
                                         Length(max=20, message='Название платформы должно быть не '
                                                                'длиннее 20 символов')])
    developer = StringField('Разработчик',
                            [InputRequired('Это поле обязательно'),
                             Length(max=127, message='Имя разработчика должно быть не '
                                                     'длиннее 127 символов')])
    release_date = DateField('Дата релиза игры', [InputRequired('Это поле обязательно')])
    in_stock = IntegerField('Количество на складе',
                            [NumberRange(0, message='Количество должно быть неотрицательным')],
                            default=0)
    is_deleted = BooleanField('Товар удалён')
    submit = SubmitField('Создать товар')
