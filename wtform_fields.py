# -*- coding=utf-8 -*-
# !/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired,  Length, EqualTo, ValidationError

from passlib.hash import pbkdf2_sha256
from models import User


def invalid_credentials(form, field):
    """ Перевірка імені користувача та пароля """

    username = form.username.data
    password = field.data

    # Реєстраційні дані недійсні
    user_data = User.query.filter_by(username=username).first()
    if user_data is None:
        raise ValidationError("Ім'я або пароль невірні.")

    # Перевірте недійсний пароль
    elif not pbkdf2_sha256.verify(password, user_data.hashed_pswd):
        raise ValidationError("Ім'я або пароль невірні.")


class LoginForm(FlaskForm):
    """ Форма для входу """

    username = StringField('username', validators=[
                           InputRequired(message="Потрібне ім’я користувача")])
    password = PasswordField('password', validators=[InputRequired(message="Потрібен пароль"),
                                                     invalid_credentials])


class RegistrationForm(FlaskForm):
    """Реєстраційна форма"""

    username = StringField('username', validators=[InputRequired(message="Потрібне ім’я користувача"),
                                                   Length(min=4, max=25, message="Ім'я має бути від 4 до 25 символів")])
    password = PasswordField('password', validators=[InputRequired(message="Потрібен пароль"),
                                                     Length(min=4, max=25, message="Пароль має бути від 4 до 25 символів")])
    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Потрібен пароль"),
                                                             EqualTo('password', message="Паролі повинні співпадати")])

    def validate_username(self, username):
        """ Перевірка, чи існує ім'я користувача """
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError(
                "Ім'я користувача вже існує. Виберіть інше ім’я користувача.")
