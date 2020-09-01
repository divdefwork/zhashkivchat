# -*- coding=utf-8 -*-
# !/usr/bin/env python3

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'replace later'


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
