from django.test import TestCase
from django.contrib.auth.models import User
from exercises.models import Exercise
from workouts.models import Workout, WorkoutExercise
from datetime import  timedelta
from django.utils import timezone

class WorkoutModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_workout_minimal(self):
        workout = Workout.objects.create(user=self.user, name="Morning Workout", type="Cardio")
        self.assertEqual(workout.user, self.user)
        self.assertEqual(workout.name, "Morning Workout")
        self.assertEqual(workout.type, "Cardio")
        self.assertIsNotNone(workout.date)
        self.assertIsNone(workout.completed_date)
        self.assertIsNone(workout.duration)  # DurationField defaults to 0 duration

    def test_str_method(self):
        workout = Workout.objects.create(user=self.user, name="Leg Day", type="Strength")
        expected_str = f"Leg Day - {workout.date}"
        self.assertEqual(str(workout), expected_str)

    def test_completed_date_and_duration(self):
        workout = Workout.objects.create(
            user=self.user,
            name="Evening Workout",
            type="HIIT",
            duration=timedelta(minutes=45),
            completed_date=None
        )
        self.assertEqual(workout.duration, timedelta(minutes=45))
        self.assertIsNone(workout.completed_date)

        # Set completed_date and test
        now = timezone.now()
        workout.completed_date = now
        workout.save()
        workout.refresh_from_db()
        self.assertEqual(workout.completed_date, now)


class WorkoutExerciseModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpass2')
        self.workout = Workout.objects.create(user=self.user, name="Full Body", type="Strength")
        self.exercise = Exercise.objects.create(name="Push Up", category="Push", muscles_targeted="Chest")

    def test_create_workout_exercise_defaults(self):
        workout_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise
        )
        self.assertEqual(workout_exercise.sets, 3)
        self.assertEqual(workout_exercise.reps, 10)
        self.assertEqual(workout_exercise.weight, 0)
        self.assertIsNone(workout_exercise.super_set_group)
        self.assertEqual(workout_exercise.order, 1)
        self.assertEqual(workout_exercise.notes, '')

    def test_str_method(self):
        workout_exercise = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            order=2
        )
        expected_str = f"{self.exercise.name} in {self.workout.name}"
        self.assertEqual(str(workout_exercise), expected_str)

    def test_ordering_of_workout_exercises(self):
        ex2 = Exercise.objects.create(name="Squat", category="Legs")
        we1 = WorkoutExercise.objects.create(workout=self.workout, exercise=self.exercise, order=2)
        we2 = WorkoutExercise.objects.create(workout=self.workout, exercise=ex2, order=1)
        exercises_ordered = list(self.workout.workout_exercises.all())
        self.assertEqual(exercises_ordered, [we2, we1])  # Should be ordered by 'order' ascending

    def test_superset_group_can_be_set(self):
        we = WorkoutExercise.objects.create(
            workout=self.workout,
            exercise=self.exercise,
            super_set_group=1
        )
        self.assertEqual(we.super_set_group, 1)
