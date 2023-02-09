from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import length, InputRequired, Email, EqualTo

from auth.models import User


class AuthForm(FlaskForm):
    email = EmailField('Почта', [InputRequired('Это поле обязательно'),
                                 Email('Введите корректный адрес электронной почты',
                                       check_deliverability=True)])
    password = PasswordField('Пароль', [InputRequired('Это поле обязательно'),
                                        length(6, message='Длина пароля должна быть '
                                                          'не менее 6 символов')])


class RegisterForm(AuthForm):
    second_password = PasswordField('Подтверждение пароля',
                                    [InputRequired('Это поле обязательно'),
                                     length(6, message='Длина пароля должна быть '
                                                       'не менее 6 символов'),
                                     EqualTo('password', 'Пароли не совпадают')])
    button = SubmitField('Зарегистрироваться')

    def validate(self, extra_validators=None):
        validated = super().validate(extra_validators=extra_validators)
        if not validated:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Пользователь с такой почтой уже существует')
            return False

        return True


class LoginForm(AuthForm):
    remember = BooleanField('Запомнить меня')
    button = SubmitField('Авторизоваться')
