import flask_login.mixins
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, EmailField, TextAreaField
import datetime
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from data import db_session
from data.users import User
from data.messages import Message


app = Flask(__name__)
app.config['SECRET_KEY'] = 'zxczxczxc'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/vseti.db")


@app.errorhandler(401)
def not_found_error(error):
    return login()


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = StringField('Возраст пользователя', validators=[DataRequired()])
    info = TextAreaField("Немного о себе", validators=[DataRequired()])
    submit = SubmitField('Войти')


class SendMesForm(FlaskForm):
    text = StringField("Ваш текст", validators=[DataRequired()])
    submit = SubmitField('Отправить')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return index()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            info=form.info.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = SendMesForm()
    if form.validate_on_submit():
        message = Message(
            sender_name=current_user.name,
            text=form.text.data,
            sender_id=current_user.id,
            time=datetime.datetime.now(),
        )
        db_sess = db_session.create_session()
        db_sess.add(message)
        db_sess.commit()
        form.text.data = ''
    return render_template('chat.html', title='Чат', form=form,
                               zxc=db_session.create_session().query(Message))


@app.route('/<user_input>')
def zxc(user_input):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_input).first()
    if user:
        params = {
            'id': user.id,
            'surname': user.surname,
            'name': user.name,
            'age': user.age,
            'info': user.info
        }
        return render_template('profile.html', **params)
    else:
        return 'Пользователь не найден'


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
