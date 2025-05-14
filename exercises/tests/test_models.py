from django.test import TestCase
from django.core.exceptions import ValidationError
from workouts.models import Exercise

class ExerciseModelTest(TestCase):

    def test_create_exercise_with_valid_data(self):
        exercise = Exercise.objects.create(
            name="Bench Press",
            category="Push",
            muscles_targeted="Chest, Triceps",
            duration=120
        )
        self.assertEqual(exercise.name, "Bench Press")
        self.assertEqual(exercise.category, "Push")
        self.assertEqual(exercise.muscles_targeted, "Chest, Triceps")
        self.assertEqual(exercise.duration, 120)

    def test_name_is_required(self):
        exercise = Exercise(
            name="",  # empty name
            category="Pull"
        )
        with self.assertRaises(ValidationError):
            exercise.full_clean()

    def test_category_is_required(self):
        exercise = Exercise(
            name="Deadlift",
            category=""  # empty category
        )
        with self.assertRaises(ValidationError):
            exercise.full_clean()

    def test_category_must_be_valid_choice(self):
        exercise = Exercise(
            name="Jumping Jacks",
            category="Cardio"  # invalid category
        )
        with self.assertRaises(ValidationError):
            exercise.full_clean()

    def test_muscles_targeted_can_be_blank_or_null(self):
        exercise1 = Exercise.objects.create(
            name="Squat",
            category="Legs",
            muscles_targeted=None
        )
        exercise2 = Exercise.objects.create(
            name="Lunges",
            category="Legs",
            muscles_targeted=""
        )
        self.assertIsNone(exercise1.muscles_targeted)
        self.assertEqual(exercise2.muscles_targeted, "")

    def test_duration_can_be_blank_or_null(self):
        exercise1 = Exercise.objects.create(
            name="Plank",
            category="Push",
            duration=None
        )
        exercise2 = Exercise.objects.create(
            name="Wall Sit",
            category="Legs"
            # duration omitted, defaults to None
        )
        self.assertIsNone(exercise1.duration)
        self.assertIsNone(exercise2.duration)

    def test_str_method_returns_name(self):
        exercise = Exercise(
            name="Overhead Press",
            category="Push"
        )
        self.assertEqual(str(exercise), "Overhead Press")
