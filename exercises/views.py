from rest_framework import viewsets
from .models import Exercise
from .serializers import ExerciseSerializer

# Create your views here.
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer