from flask import Flask, render_template
from flask import request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user
from data import db_session
from data.users import User
app = Flask(__name__)
app.config['SECRET_KEY'] = 'zxczxczxc'
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/mars_explorer.db")

class OldLoginForm(FlaskForm):
    surname = StringField('Имя', validators=[DataRequired()])
    name = StringField('Фамилия', validators=[DataRequired()])
    education = SelectField('Образование', choices=[('Начальное','Начальное'),
                                                    ('Среднее', 'Среднее'),
                                                    ('Средне-специальное', 'Средне-специальное'),
                                                    ('Высшее', 'Высшее')])
    profession = SelectField('Профессия', choices=[('Пилот','Пилот'),
                                                    ('Строитель', 'Строитель'),
                                                    ('Экзобиолог', 'Экзобиолог'),
                                                    ('Киберинженер', 'Киберинженер')])
    sex = SelectField('Пол', choices=[('Мужчина','Мужчина'),
                                                    ('Женщина', 'Женщина')])
    motivation = StringField('Мотивация', validators=[DataRequired()])
    ready = SelectField('Готов остаться на марте?', choices=[('ДА','ДА'),
                                                    ('НЕТ', 'НЕТ')])
    submit = SubmitField('Войти')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return list_prof('ol')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('auto_answer.html', form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/<user_input>')
def zxc(user_input):
    params = {
        'title': user_input,
        'news':['qwe', 'asd', 'fgh']
    }
    return render_template('index4.html', **params)
@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести! "
@app.route('/image_mars')
def image_mars():
    return render_template("index.html")
@app.route('/promotion')
def promotion():
    return "Человечество вырастает из детства.     <br>Человечеству мала одна планета.<br>Мы сделаем обитаемыми безжизненные пока планеты.<br>И начнем с Марса!<br>Присоединяйся!"
@app.route('/promotion_image')
def promotion_image():
    return render_template("index2.html")

@app.route('/training/<zxc>')
def training(zxc):
    return render_template("index5.html", zxc=zxc)
@app.route('/list_prof/<zxc>')
def list_prof(zxc):
    return render_template("index6.html", zxc=zxc)
@app.route('/asronaut_selection', methods=['GET', 'POST'])
def asronaut_selection():
    if request.method == 'GET':
        return render_template("index3.html")
    elif request.method == 'POST':
        for key, value in request.form.items():
            print(value)
        return render_template("index3.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
