from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from models import db

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = text("SELECT id, password FROM users WHERE username = :username")
        result = db.session.execute(sql, {"username": username}).fetchone()
        if result:
            user_id, stored_password = result
            if check_password_hash(stored_password, password):
                session['user_id'] = user_id
                flash('You were successfully logged in')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password')
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = text("SELECT username FROM users WHERE username = :username")
        result = db.session.execute(sql, {"username": username})
        user_exists = result.fetchone()
        if user_exists:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        hash_password = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username": username, "password": hash_password})
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))

