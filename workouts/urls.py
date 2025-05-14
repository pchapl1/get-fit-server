from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutViewSet

# Set up the router and register the Workout viewset
router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet)
# router.register(r'workout_exercises', WorkoutExerciseViewSet, basename='workoutexercise')

urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
]
