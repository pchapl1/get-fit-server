from django.db import models
from django.contrib.auth.models import User
from exercises.models import Exercise    

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate workout with a user
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)  # Auto set the date when created
    duration = models.DurationField(blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(default=10)
    weight = models.IntegerField(default=0)
    super_set_group = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exercise.name} in {self.workout.name}"


