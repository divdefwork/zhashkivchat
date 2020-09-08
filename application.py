# -*- coding=utf-8 -*-
# !/usr/bin/env python3

import time
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_socketio import SocketIO, join_room, leave_room, send

from wtform_fields import *
from models import *

# Налаштування програми
app = Flask(__name__)
app.secret_key = 'replace later'

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ywqxdfutjbrllu:4bf9490496b00c99e12a00ac7aad76018a943dd7997fb6667da8dc33b63dd075@ec2-54-228-209-117.eu-west-1.compute.amazonaws.com:5432/dc4d1f73beffi3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ініціалізуйте Flask-SocketIO
# socketio = SocketIO(app)
# ROOMS = ["вітальня", "продам/куплю", "реклама", "питання/відповідь"]

# Налаштування flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):

    return User.query.get(int(id))


socketio = SocketIO(app, manage_session=False)

# Наперед визначені кімнати для чату
ROOMS = ["вітальня", "продам/куплю", "реклама", "питання/відповідь"]


@app.route('/', methods=['GET', 'POST'])
def index():

    login_form = LoginForm()

    # Дозволити увійти, якщо успішна перевірка
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template('index.html', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    reg_form = RegistrationForm()

    # Оновлення бази даних, якщо успішна перевірка
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Хеш пароля
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Додати користувача в БД
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Зареєстровано успішно. Будь ласка, увійдіть.', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=reg_form, title="Реєстрація")


@app.route('/chat', methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Будь ласка, увійдіть', 'danger')
        return redirect(url_for('index'))

    return render_template('chat.html',
                           username=current_user.username, rooms=ROOMS)


@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('Ви успішно вийшли з системи', 'success')
    return redirect(url_for('index'))


@socketio.on('incoming-msg')
def on_message(data):
    """Трансляція повідомлень"""

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Встановити позначку часу
    time_stamp = time.strftime('%H:%M %d %B', time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)


@socketio.on('join')
def on_join(data):
    """Користувач приєднується до кімнати"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Трансляція, до якої приєднався новий користувач
    send({"msg": username + " приєднався до кімнати" + room + "."}, room=room)


@socketio.on('leave')
def on_leave(data):
    """Користувач залишає кімнату"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " вийшов із кімнати"}, room=room)


if __name__ == "__main__":
    # socketio.run(app, debud=True)
    app.run(debug=True)
