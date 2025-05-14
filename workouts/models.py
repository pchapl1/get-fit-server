from django.db import models
from django.contrib.auth.models import User
from exercises.models import Exercise    

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate workout with a user
    name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)  # Auto set the date when created
    duration = models.DurationField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.IntegerField()
    notes = models.TextField(blank=True)


