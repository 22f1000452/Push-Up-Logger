from flask import Blueprint, flash, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
  return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')

  user = User.query.filter_by(email=email).first()
  if user:
    flash("User already exists, Please Use Different Email...", 'warning')
    return redirect(url_for('auth.signup'))

  password = generate_password_hash(password, method='scrypt')

  user = User(name=name, email=email, password=password)

  db.session.add(user)
  db.session.commit()

  # print(f"Name: {name}, Email: {email}, Password: {password}")
  return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
  return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
  email = request.form.get('email')
  password = request.form.get('password')
  remember = True if request.form.get('remember') else False

  user = User.query.filter_by(email=email).first()

  if not user:
    flash("User not found", 'danger')
    return redirect(url_for('auth.login'))
  elif not check_password_hash(user.password, password):
    flash("Incorrect password, Please try again...", 'danger')
    return redirect(url_for('auth.login'))

  login_user(user, remember=remember)
  # print(f"Email: {email}, Password: {password}")
  return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
  # return "Welcome to the Push-Up Logger!"  # This line is ignored in the context of the task
  logout_user()
  return redirect(url_for('auth.login'))