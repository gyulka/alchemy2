from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField,IntegerField,DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    name = StringField('логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('войти')


class NewJob(FlaskForm):
    description = TextAreaField('описание', validators=[DataRequired()])
    team_leader = IntegerField('team_leader id')
    team = StringField('id участников команды')
    startdate= DateField('Дата начала')
    is_finished = BooleanField('работа закончена?')

    submit = SubmitField('создать')

class EditJob(NewJob):
    submit = SubmitField('изменить')

class NewDep(FlaskForm):
    email = EmailField('почта')
    title = StringField('название')
    chief = IntegerField('id шефа')
    team = StringField('id членов команды')

    submit = SubmitField('создать')

class EditDep(NewDep):
    submit = SubmitField('изменить')