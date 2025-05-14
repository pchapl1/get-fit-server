from django.db import models

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=[('Push', 'Push'), ('Pull', 'Pull'), ('Legs', 'Legs')])
    muscles_targeted = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in seconds", blank=True, null=True)
    
    def __str__(self):
        return self.name