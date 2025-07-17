from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from datetime import datetime

from app import db
from app.models import User
from app.models import Workout

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.name)

@main.route('/workouts')
@login_required
def workouts():
  workouts = Workout.query.filter_by(user_id=current_user.id).all()
  return render_template('workouts.html', workouts=workouts)

@main.route('/workout/new')
@login_required
def new_workout():
  return render_template('new_workout.html')

@main.route('/workout/new', methods=['POST'])
@login_required
def new_workout_post():
  pushup = int(request.form.get('pushups'))
  comment = request.form.get('comments')
  date = request.form.get('date')
  workout = Workout(user_id=current_user.id, date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'), pushups=pushup, comments=comment, user=current_user)
  db.session.add(workout)
  db.session.commit()

  flash('Workout added successfully!', 'success')
  return redirect(url_for('main.workouts'))

@main.route('/workout/update/<int:workout_id>')
@login_required
def update_workout(workout_id):
  workout = Workout.query.get_or_404(workout_id)
  # if workout.user_id != current_user.id:
  #   flash('You do not have permission to edit this workout.', 'danger')
  #   return redirect(url_for('main.workouts'))

  return render_template('update_workout.html', workout=workout)

@main.route('/workout/update/<int:workout_id>', methods=['POST'])
@login_required
def update_workout_post(workout_id):
  workout = Workout.query.get_or_404(workout_id)
  # if workout.user_id != current_user.id:
  #   flash('You do not have permission to edit this workout.', 'danger')
  #   return redirect(url_for('main.workouts'))

  workout.pushups = int(request.form.get('pushups'))
  workout.comments = request.form.get('comments')
  workout.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d %H:%M:%S')

  db.session.commit()

  flash('Workout updated successfully!', 'success')
  return redirect(url_for('main.workouts'))

@main.route('/workout/delete/<int:workout_id>')
@login_required
def delete_workout(workout_id):
  workout = Workout.query.get_or_404(workout_id)
  if workout.user_id != current_user.id:
    flash('You do not have permission to delete this workout.', 'danger')
    return redirect(url_for('main.workouts'))

  db.session.delete(workout)
  db.session.commit()

  flash('Workout deleted successfully!', 'success')
  return redirect(url_for('main.workouts'))

