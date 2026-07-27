from flask import request, jsonify, make_response
from marshmallow import ValidationError

from app import app
from app.models import db, Workout, Exercise, WorkoutExercise
from app.scheema import (
    workout_schema, workouts_schema,
    exercise_schema, exercises_schema,
    workout_exercise_schema
)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return workout_schema.dump(workout), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        data = workout_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    try:
        workout = Workout(
            date=data['date'],
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(workout)
        db.session.commit()
        return workout_schema.dump(workout), 201
    except (ValueError, Exception) as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout deleted successfully"}), 200)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return exercise_schema.dump(exercise), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        data = exercise_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    try:
        exercise = Exercise(
            name=data['name'],
            category=data.get('category'),
            equipment_needed=data['equipment_needed']
        )
        db.session.add(exercise)
        db.session.commit()
        return exercise_schema.dump(exercise), 201
    except (ValueError, Exception) as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise deleted successfully"}), 200)


def _add_exercise_to_workout(workout, exercise, metric_data):
    existing = WorkoutExercise.query.filter_by(
        workout_id=workout.id,
        exercise_id=exercise.id
    ).first()
    if existing:
        return None, make_response(jsonify({"error": "Exercise already exists in this workout"}), 409)

    try:
        we = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            sets=metric_data.get('sets'),
            reps=metric_data.get('reps'),
            duration_seconds=metric_data.get('duration_seconds')
        )
        db.session.add(we)
        db.session.commit()
        return workout_schema.dump(workout), 201
    except (ValueError, Exception) as e:
        db.session.rollback()
        return None, make_response(jsonify({"error": str(e)}), 400)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        metric_data = workout_exercise_schema.load({**json_data, "exercise_id": exercise_id})
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    response, status = _add_exercise_to_workout(workout, exercise, metric_data)
    return response, status


@app.route('/workouts/<int:workout_id>/exercises', methods=['POST'])
def add_exercise_to_workout_alias(workout_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        metric_data = workout_exercise_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    exercise = db.session.get(Exercise, metric_data['exercise_id'])
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    response, status = _add_exercise_to_workout(workout, exercise, metric_data)
    return response, status


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Resource not found"}), 404)


@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({"error": "Method not allowed"}), 405)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

