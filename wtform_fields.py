# -*- coding=utf-8 -*-
# !/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired,  Length, EqualTo, ValidationError

from models import User


class RegistrationForm(FlaskForm):
    """Реєстраційна форма"""

    username = StringField('username_label',
                           validators=[InputRequired(message="Потрібне ім’я користувача"),
                                       Length(min=4, max=25, message="Ім'я має бути від 4 до 25 символів")])
    password = PasswordField('password_label',
                             validators=[InputRequired(message="Потрібен пароль"),
                                         Length(min=4, max=25, message="Пароль має бути від 4 до 25 символів")])
    confirm_pswd = PasswordField('confirm_pswd_label',
                                 validators=[InputRequired(message="Потрібен пароль"),
                                             EqualTo('password', message="Паролі повинні співпадати")])
    submit_button = SubmitField('Створити')

    def validate_username(self, username):
        """ Перевірка, чи існує ім'я користувача """
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError(
                "Ім'я користувача вже існує. Виберіть інше ім’я користувача.")
