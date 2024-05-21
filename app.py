from flask import Flask, request, render_template, url_for, abort, redirect, flash, session
from werkzeug.utils import secure_filename
from pathlib import PurePath, Path
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()


@app.route('/')
def index_func():
    if 'username' in session:
        return redirect(url_for('hello_func'))
    return redirect(url_for('login_func'))


@app.route('/login/', methods=['GET', 'POST'])
def login_func():
    if request.method == 'POST':
        session['username'] = request.form.get('username') or 'NoName'
        session['email'] = request.form.get('email') or 'NoEmail'
        return redirect(url_for('index_func'))
    return render_template('username_form.html', title='Авторизация')


@app.route('/logout/')
def logout_func():
    session.pop('username', None)
    return redirect(url_for('index_func'))


@app.route('/hello/')
def hello_func():
    if session.get('username', False):
        context = {
            'title': 'Привет',
            'username': session['username'],
        }
        return render_template('hello.html', **context)
    abort(403)


@app.errorhandler(403)
def err_403(e):
    print(e)
    return render_template('err_403.html', title='ошибка входа')


if __name__ == '__main__':
    app.run()
