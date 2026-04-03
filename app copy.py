from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import init_db, add_user, user_exists
import hashlib
import os
from database import user_exists, add_user, check_password
from flask import session, flash, redirect, url_for, request
from database import generate_nickname
from database import init_db
init_db()

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register_page():
    return render_template("register.html")


@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']

    user = user_exists(username)

    if not user:
        add_user(username, password)
        session['username'] = username
        return redirect(url_for('profile'))

    if check_password(username, password):
        session['username'] = username
        return redirect(url_for('profile'))
    else:
        flash("Пароль неправильный")
        return redirect(url_for('register_page'))
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/register')

    username = session['username']
    rank = "Bronze"

    return render_template("profile.html", username=username, rank=rank)

@app.route('/account')
def account():
    if 'username' in session:
        return redirect('/profile')
    else:
        return redirect('/register')

@app.route('/random')
def random_play():
    return render_template("random_play.html")

@app.route('/stariy')
def stariy():
    return render_template("stariy.html")

@app.route('/htp')
def htp():
    return render_template("HTP.html")

@app.route('/generate_nick')
def generate_nick():
    nickname = generate_nickname()
    return {"nickname": nickname}

from flask import session

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)