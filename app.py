import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, flash, redirect, url_for
from database import init_db, add_user, user_exists
import hashlib
import os
from database import user_exists, add_user, check_password, generate_nickname, init_db, fill_words, get_user, increase_nickname_counter, get_all_players, get_player, add_player, init_default_players
import time
from functools import lru_cache


app = Flask(__name__)
app.secret_key = "super_secret_key_123"

init_db()
fill_words()
init_default_players() 

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

    user = get_user(session['username'])
    
    if user is None:
        session.pop('username', None)
        flash("Ошибка: пользователь не найден. Пожалуйста, зарегистрируйтесь снова.")
        return redirect('/register')

    return render_template(
        "profile.html",
        username=user[0],
        nick_count=user[1]
    )

@app.route('/account')
def account():
    if 'username' in session:
        return redirect('/profile')
    else:
        return redirect('/register')

@app.route('/random')
def random_play():
    return render_template("editor.html")

import requests
from flask import jsonify

YOUTUBE_API_KEY = "AIzaSyBvbeWj-3Svns8cJ0oX3-BwmUxdkir29_Q"


@lru_cache(maxsize=32)
def get_cached_video(channel_id, timestamp):
    return get_latest_video(channel_id)

def get_latest_video(channel_id):
    if not channel_id:
        return None

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': YOUTUBE_API_KEY,
        'channelId': channel_id,
        'part': 'snippet',
        'order': 'date',
        'maxResults': 1,
        'type': 'video'
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        
        data = response.json()
        
        if 'error' in data:
            print(f"Ошибка API: {data['error']['message']}")
            return None
            
        if 'items' in data and len(data['items']) > 0:
            video = data['items'][0]
            video_id = video['id']['videoId']
            print(f"видео: {video['snippet']['title'][:50]}...")
            return {
                'video_id': video_id,
                'title': video['snippet']['title'],
                'thumbnail': video['snippet']['thumbnails']['medium']['url'],
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
        else:
            print(f"Видео не найдены для канала {channel_id}")
    except requests.exceptions.Timeout:
        print(f"Таймаут запроса")
    except Exception as e:
        print(f"Ошибка получения видео: {e}")
    
    return None

def get_latest_video(channel_id):
    if not channel_id:
        return None
    
    url = f"https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': YOUTUBE_API_KEY,
        'channelId': channel_id,
        'part': 'snippet',
        'order': 'date',
        'maxResults': 1,
        'type': 'video'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            video = data['items'][0]
            video_id = video['id']['videoId']
            return {
                'video_id': video_id,
                'title': video['snippet']['title'],
                'thumbnail': video['snippet']['thumbnails']['medium']['url'],
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
    except Exception as e:
        print(f"Ошибка получения видео: {e}")
    
    return None

@app.route('/players')
def players_page():
    players = get_all_players()
    players_with_videos = []
    
    current_hour = int(time.time() / 3600)
    
    for player in players:
        player_dict = {
            'id': player[0],
            'nickname': player[1],
            'avatar': player[2] if player[2] else "/static/sprites/default_avatar.svg",
            'youtube_channel_id': player[3],
            'description': player[4] if player[4] else "",
            'latest_video': None
        }
        
        if player_dict['youtube_channel_id']:
            video = get_cached_video(player_dict['youtube_channel_id'], current_hour)
            player_dict['latest_video'] = video
        
        players_with_videos.append(player_dict)
    
    return render_template("players.html", players=players_with_videos)

@app.route('/api/refresh_video/<int:player_id>')
def refresh_video(player_id):
    player = get_player(player_id)
    if player and player[3]:
        get_cached_video.cache_clear()
        current_hour = int(time.time() / 3600)
        video = get_cached_video(player[3], current_hour)
        return jsonify(video)
    return jsonify(None)

@app.route('/htp')
def htp():
    return render_template("HTP.html")

@app.route('/generate_nick')
def generate_nick():
    nickname = generate_nickname()

    if 'username' in session:
        try:
            increase_nickname_counter(session['username'])
        except Exception as e:
            print(f"Ошибка при увеличении счетчика: {e}")

    return jsonify({"nickname": nickname})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)