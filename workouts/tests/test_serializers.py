from django.test import TestCase
from django.contrib.auth.models import User
from workouts.models import Workout, WorkoutExercise
from exercises.models import Exercise
from workouts.serializers import WorkoutSerializer, WorkoutExerciseSerializer
from datetime import timedelta

class WorkoutSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.workout = Workout.objects.create(
            user=self.user,
            name="Leg Day",
            type="Strength",
            duration=timedelta(minutes=45)
        )
        self.exercise = Exercise.objects.create(
            name="Squat",
            category="Legs",
            muscles_targeted="Quads"
        )
        self.workout_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            sets=4,
            reps=12,
            weight=100
        )

    def test_workout_exercise_serializer(self):
        serializer = WorkoutExerciseSerializer(instance=self.workout_exercise)
        expected_data = {
            "exercise": {
                "id": self.exercise.id,
                "name": "Squat",
                "category": "Legs",
                "muscles_targeted": "Quads",
                "duration": None,
            },
            "sets": 4,
            "reps": 12,
            "weight": 100
        }
        # The test will fail unless the WorkoutExerciseSerializer is updated to be a ModelSerializer
        self.assertEqual(serializer.data, expected_data)

    def test_workout_serializer_with_nested_exercises(self):
        serializer = WorkoutSerializer(instance=self.workout)
        self.assertEqual(serializer.data["name"], "Leg Day")
        self.assertEqual(serializer.data["type"], "Strength")
        self.assertEqual(serializer.data["user"], self.user.id)
        self.assertEqual(len(serializer.data["exercises"]), 1)

        nested_ex = serializer.data["exercises"][0]
        self.assertEqual(nested_ex["sets"], 4)
        self.assertEqual(nested_ex["reps"], 12)
        self.assertEqual(nested_ex["weight"], 100)
        self.assertEqual(nested_ex["exercise"]["name"], "Squat")
