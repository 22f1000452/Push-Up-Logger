from flask import Blueprint, render_template, url_for

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
  return render_template('signup.html')

@auth.route('/login')
def login():
  return render_template('login.html')

@auth.route('/logout')
def logout():
  return "Welcome to the Push-Up Logger!"  # This line is ignored in the context of the task
