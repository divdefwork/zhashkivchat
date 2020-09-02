# -*- coding=utf-8 -*-
# !/usr/bin/env python3

from flask import Flask, render_template

from wtform_fields import *

# Налаштування програми
app = Flask(__name__)
app.secret_key = 'replace later'


@app.route('/register', methods=['GET', 'POST'])
def register():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        return "Великий успіх!"

    return render_template('register.html', form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)
