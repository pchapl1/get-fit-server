from django.test import TestCase
from rest_framework.exceptions import ValidationError
from exercises.serializers import ExerciseSerializer

class ExerciseSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            "name": "Bench Press",
            "category": "Push",
            "muscles_targeted": "Chest, Triceps",
            "duration": 120
        }
        self.invalid_category_data = {
            "name": "Jump Rope",
            "category": "Cardio",  # invalid category
            "muscles_targeted": "Legs",
            "duration": 60
        }
        self.missing_name_data = {
            "category": "Pull",
            "muscles_targeted": "Back",
            "duration": 90
        }

    def test_serializer_valid_data(self):
        serializer = ExerciseSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        exercise = serializer.save()
        self.assertEqual(exercise.name, self.valid_data['name'])
        self.assertEqual(exercise.category, self.valid_data['category'])
        self.assertEqual(exercise.muscles_targeted, self.valid_data['muscles_targeted'])
        self.assertEqual(exercise.duration, self.valid_data['duration'])

    def test_serializer_missing_required_field_name(self):
        serializer = ExerciseSerializer(data=self.missing_name_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_serializer_invalid_category_choice(self):
        serializer = ExerciseSerializer(data=self.invalid_category_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category', serializer.errors)

    def test_serializer_update_instance(self):
        serializer = ExerciseSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        exercise = serializer.save()

        update_data = {
            "name": "Incline Bench Press",
            "category": "Push",
            "muscles_targeted": "Upper Chest",
            "duration": 150
        }
        serializer = ExerciseSerializer(instance=exercise, data=update_data)
        self.assertTrue(serializer.is_valid())
        updated_exercise = serializer.save()

        self.assertEqual(updated_exercise.name, update_data['name'])
        self.assertEqual(updated_exercise.category, update_data['category'])
        self.assertEqual(updated_exercise.muscles_targeted, update_data['muscles_targeted'])
        self.assertEqual(updated_exercise.duration, update_data['duration'])
