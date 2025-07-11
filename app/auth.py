from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash
from app import db
from app.models import User

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
    print("User already exists")
    return redirect(url_for('auth.signup'))

  password = generate_password_hash(password, method='sha256')

  user = User(name=name, email=email, password=password)

  db.session.add(user)
  db.session.commit()

  print(f"Name: {name}, Email: {email}, Password: {password}")
  return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
  return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
  email = request.form.get('email')
  password = request.form.get('password')

  user = User.query.filter_by(email=email).first()

  if not user:
    print("User not found")
    return redirect(url_for('auth.login'))

  if user.password != password:
    print("Incorrect password")
    return redirect(url_for('auth.login'))

  print(f"Email: {email}, Password: {password}")
  return redirect(url_for('main.profile'))

@auth.route('/logout')
def logout():
  return "Welcome to the Push-Up Logger!"  # This line is ignored in the context of the task
