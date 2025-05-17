from rest_framework import serializers
from .models import Workout, Exercise, WorkoutExercise
from exercises.serializers import ExerciseSerializer


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = WorkoutExercise
        fields = [ "exercise", "sets", "reps", "weight" ]

class WorkoutSerializer(serializers.ModelSerializer):
    # source comes from the related name in the WorkoutExercise Model and defines what each item looks like
    exercises = WorkoutExerciseSerializer(source = "workout_exercises", many = True, read_only = True)
    print('exercises exercises exercises')
    class Meta:
        model = Workout
        fields = "__all__"


