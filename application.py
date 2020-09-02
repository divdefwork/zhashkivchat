# -*- coding=utf-8 -*-
# !/usr/bin/env python3

from flask import Flask, render_template

from wtform_fields import *
from models import *

# Налаштування програми
app = Flask(__name__)
app.secret_key = 'replace later'

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ywqxdfutjbrllu:4bf9490496b00c99e12a00ac7aad76018a943dd7997fb6667da8dc33b63dd075@ec2-54-228-209-117.eu-west-1.compute.amazonaws.com:5432/dc4d1f73beffi3'
db = SQLAlchemy(app)


@app.route('/register', methods=['GET', 'POST'])
def register():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Перевірте, чи існує ім’я користувача
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Хтось інший взяв це ім’я користувача!"

        # Додати користувача в БД
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Додано до БД!"

    return render_template('register.html', form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)
