from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(200), nullable=False)

class Workout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  date = db.Column(db.DateTime, nullable=False)
  pushups = db.Column(db.Integer, nullable=False)
  comments = db.Column(db.String(200), nullable=True)
  user = db.relationship('User', backref=db.backref('workouts', lazy=True))