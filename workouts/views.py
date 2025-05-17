from rest_framework import viewsets
from .models import Workout
from .serializers import WorkoutSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()  # Get all workouts from the database
    serializer_class = WorkoutSerializer  # Use the WorkoutSerializer to convert to/from JSON
    def list(self, request, *args, **kwargs):
        print("WorkoutViewSet list called")   # Check if this prints
        print(f"Number of workouts: {self.queryset.count()}")
        return super().list(request, *args, **kwargs)

