# -*- coding=utf-8 -*-
# !/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for

from wtform_fields import *
from models import *

# Налаштування програми
app = Flask(__name__)
app.secret_key = 'replace later'

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ywqxdfutjbrllu:4bf9490496b00c99e12a00ac7aad76018a943dd7997fb6667da8dc33b63dd075@ec2-54-228-209-117.eu-west-1.compute.amazonaws.com:5432/dc4d1f73beffi3'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():

    login_form = LoginForm()

    # Дозволити увійти, якщо успішна перевірка
    if login_form.validate_on_submit():
        return "Ввійшли успішно!"

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

        return redirect(url_for('index'))

    return render_template('register.html', form=reg_form, title="Реєстрація")


if __name__ == "__main__":
    app.run(debug=True)
