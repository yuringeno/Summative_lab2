# Workout Tracker API

A Flask-based RESTful API for tracking workouts and exercises. Built with Flask, SQLAlchemy, and Marshmallow, this application enables personal trainers to create workouts, define reusable exercises, and associate exercises with workouts including sets, reps, and duration metrics.

## Description

This backend API provides a complete workout management system with:

- **Workouts**: Create, view, and delete workout sessions
- **Exercises**: Create, view, and delete reusable exercises (can be shared across multiple workouts)
- **Workout-Exercises**: Add exercises to workouts with configurable sets, reps, or duration

The application features multiple layers of validation:
- **Database Constraints**: Unique exercise names, positive numeric checks on sets/reps/duration
- **Model Validations**: Name presence checks, metric requirements
- **Schema Validations**: Length constraints, range validations, custom validators

## Installation Instructions

### Prerequisites
- Python 3.8.13+
- Pipenv

### Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd Summative_lab2

# 2. Install dependencies using Pipenv
pipenv install

# 3. Activate the virtual environment
pipenv shell

# 4. Initialize the database and run migrations
export FLASK_APP=server.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 5. Seed the database with example data
python seed.py
```

## Run Instructions

```bash
# Ensure the virtual environment is active
pipenv shell

# Start the Flask development server
flask run

# Or run directly
python server.py
```

The server will start at `http://localhost:5000` (or port 5555 if using `python server.py`).

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/workouts` | Retrieve all workouts |
| `GET` | `/workouts/<id>` | Retrieve a single workout by ID (includes exercises) |
| `POST` | `/workouts` | Create a new workout |
| `DELETE` | `/workouts/<id>` | Delete a workout by ID |

**POST /workouts** request body:
```json
{
  "date": "2026-07-27",
  "duration_minutes": 60,
  "notes": "A comprehensive full body workout"
}
```

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/exercises` | Retrieve all exercises |
| `GET` | `/exercises/<id>` | Retrieve a single exercise by ID |
| `POST` | `/exercises` | Create a new exercise |
| `DELETE` | `/exercises/<id>` | Delete an exercise by ID |

**POST /exercises** request body:
```json
{
  "name": "Push Up",
  "category": "Strength",
  "equipment_needed": false
}
```

### Workout-Exercises (Add Exercise to Workout)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an existing exercise to a workout with metrics |

**POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises** request body:
```json
{
  "sets": 3,
  "reps": 15,
  "duration_seconds": 120
}
```

At least one metric (`sets`, `reps`, or `duration_seconds`) must be provided.

## Validations

### Table Constraints
- `UNIQUE(name)` on `Exercise` prevents duplicate exercise names
- `CHECK(duration_minutes > 0)` on `Workout` ensures positive workout duration
- `CHECK(sets > 0)` ensures sets are positive
- `CHECK(reps > 0)` ensures reps are positive
- `CHECK(duration_seconds > 0)` ensures exercise duration is positive

### Model Validations
- `Workout.date` must be present
- `Workout.duration_minutes` must be positive when provided
- `Exercise.name` must not be empty
- `WorkoutExercise` must include at least one metric (`sets`, `reps`, or `duration_seconds`)

### Schema Validations
- Exercise name must be 1-100 characters and not blank
- Workout duration must be positive when provided
- `equipment_needed` is required for exercises
- WorkoutExercise requires at least one of `sets`, `reps`, or `duration_seconds`

## Project Structure

```
├── app/
│   ├── __init__.py      # Flask app initialization
│   ├── models.py         # SQLAlchemy models (Workout, Exercise, WorkoutExercise)
│   └── scheema.py        # Marshmallow schemas for serialization/validation
├── server.py             # Flask routes and application entry point
├── seed.py               # Database seed script with example data
├── Pipfile               # Python dependencies
├── Pipfile.lock          # Locked dependency versions
├── requirements.txt      # Alternative dependency listing
├── README.md             # This file
└── .gitignore            # Git ignore rules
```

## Technologies Used

- **Flask 3.1.3** - Web framework
- **Flask-SQLAlchemy 3.1.1** - Database ORM
- **Flask-Migrate 4.1.0** - Database migrations
- **Marshmallow 4.3.0** - Object serialization/deserialization
- **SQLite** - Development database

