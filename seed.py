#!/usr/bin/env python3
"""Seed script to populate the database with example data for all models."""

from datetime import date

from app import app
from app.models import db, Workout, Exercise, WorkoutExercise


def seed_database():
    with app.app_context():
        print("Dropping all tables and recreating...")
        db.drop_all()
        db.create_all()

        print("Creating exercises...")
        push_up = Exercise(
            name="Push Up",
            category="Strength",
            equipment_needed=False
        )
        squat = Exercise(
            name="Squat",
            category="Strength",
            equipment_needed=False
        )
        plank = Exercise(
            name="Plank",
            category="Core",
            equipment_needed=False
        )
        jumping_jack = Exercise(
            name="Jumping Jack",
            category="Cardio",
            equipment_needed=False
        )
        bicep_curl = Exercise(
            name="Bicep Curl",
            category="Strength",
            equipment_needed=True
        )
        lunges = Exercise(
            name="Lunges",
            category="Strength",
            equipment_needed=False
        )

        exercises = [push_up, squat, plank, jumping_jack, bicep_curl, lunges]
        for ex in exercises:
            db.session.add(ex)
        db.session.commit()
        print(f"Created {len(exercises)} exercises.")

        print("Creating workouts...")
        full_body = Workout(
            date=date(2026, 7, 27),
            duration_minutes=60,
            notes="A comprehensive full body workout for all fitness levels."
        )
        core_strength = Workout(
            date=date(2026, 7, 28),
            duration_minutes=45,
            notes="Focus on building a strong core and improving stability."
        )
        cardio_burn = Workout(
            date=date(2026, 7, 29),
            duration_minutes=30,
            notes="High-intensity cardio workout to burn calories."
        )

        workouts = [full_body, core_strength, cardio_burn]
        for w in workouts:
            db.session.add(w)
        db.session.commit()
        print(f"Created {len(workouts)} workouts.")

        print("Adding exercises to workouts...")
        we1 = WorkoutExercise(
            workout=full_body,
            exercise=push_up,
            sets=3,
            reps=15
        )
        we2 = WorkoutExercise(
            workout=full_body,
            exercise=squat,
            sets=3,
            reps=12
        )
        we3 = WorkoutExercise(
            workout=full_body,
            exercise=lunges,
            sets=3,
            reps=10
        )
        we4 = WorkoutExercise(
            workout=core_strength,
            exercise=plank,
            sets=3,
            duration_seconds=60
        )
        we5 = WorkoutExercise(
            workout=core_strength,
            exercise=squat,
            sets=3,
            reps=15
        )
        we6 = WorkoutExercise(
            workout=cardio_burn,
            exercise=jumping_jack,
            sets=3,
            duration_seconds=90
        )
        we7 = WorkoutExercise(
            workout=cardio_burn,
            exercise=plank,
            sets=3,
            duration_seconds=45
        )

        associations = [we1, we2, we3, we4, we5, we6, we7]
        for assoc in associations:
            db.session.add(assoc)
        db.session.commit()
        print(f"Created {len(associations)} workout-exercise associations.")

        print("Database seeded successfully.")
        print("-" * 40)
        print(f"Exercises: {Exercise.query.count()}")
        print(f"Workouts: {Workout.query.count()}")
        print(f"WorkoutExercises: {WorkoutExercise.query.count()}")


if __name__ == '__main__':
    seed_database()

