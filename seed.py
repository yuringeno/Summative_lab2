#!/usr/bin/env python3
"""Seed script to populate the database with example data for all models."""

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
            description="A classic bodyweight chest exercise.",
            category="Strength"
        )
        squat = Exercise(
            name="Squat",
            description="A fundamental lower body exercise.",
            category="Strength"
        )
        plank = Exercise(
            name="Plank",
            description="A core stability exercise.",
            category="Core"
        )
        jumping_jack = Exercise(
            name="Jumping Jack",
            description="A full-body cardio warm-up exercise.",
            category="Cardio"
        )
        bicep_curl = Exercise(
            name="Bicep Curl",
            description="An isolation exercise for biceps using dumbbells.",
            category="Strength"
        )
        lunges = Exercise(
            name="Lunges",
            description="A compound lower body exercise.",
            category="Strength"
        )

        exercises = [push_up, squat, plank, jumping_jack, bicep_curl, lunges]
        for ex in exercises:
            db.session.add(ex)
        db.session.commit()
        print(f"Created {len(exercises)} exercises.")

        print("Creating workouts...")
        full_body = Workout(
            name="Full Body Blast",
            description="A comprehensive full body workout for all fitness levels."
        )
        core_strength = Workout(
            name="Core Crusher",
            description="Focus on building a strong core and improving stability."
        )
        cardio_burn = Workout(
            name="Cardio Burn",
            description="High-intensity cardio workout to burn calories."
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
            duration=60
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
            duration=90
        )
        we7 = WorkoutExercise(
            workout=cardio_burn,
            exercise=plank,
            sets=3,
            duration=45
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

