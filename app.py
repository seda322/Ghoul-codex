from flask import Flask, render_template, request
from database import init_db, add_user, user_exists
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Инициализация базы данных при запуске
init_db()

def hash_password(password):
    """Хеширование пароля для безопасности"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    # Валидация данных
    if not username or not password:
        return render_template('register.html', error="Заполните все поля")

    if len(username) < 3:
        return render_template('register.html', error="Логин должен содержать минимум 3 символа")

    if len(password) < 6:
        return render_template('register.html', error="Пароль должен содержать минимум 6 символов")

    # Проверка существования пользователя
    if user_exists(username):
        return render_template('register.html', error="Пользователь с таким логином уже существует")

    # Хеширование пароля и добавление пользователя
    hashed_password = hash_password(password)

    if add_user(username, hashed_password):
        return render_template('register.html', success="Регистрация прошла успешно!")
    else:
        return render_template('register.html', error="Ошибка при регистрации")

if __name__ == '__main__':
    app.run(debug=True)
