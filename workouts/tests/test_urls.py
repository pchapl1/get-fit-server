from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from workouts.models import Workout
from datetime import timedelta

class WorkoutURLsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.workout = Workout.objects.create(
            user=self.user,
            name="Test Workout",
            type="Strength",
            duration=timedelta(minutes=30)
        )

    def test_list_workouts_url(self):
        url = reverse('workout-list')  # This comes from the router
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_workout_url(self):
        url = reverse('workout-detail', args=[self.workout.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_workout_url(self):
        url = reverse('workout-list')
        data = {
            "user": self.user.id,
            "name": "New Workout",
            "type": "Cardio"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_workout_url(self):
        url = reverse('workout-detail', args=[self.workout.id])
        data = {
            "user": self.user.id,
            "name": "Updated Workout",
            "type": "Strength",
            "duration": "00:45:00"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_workout_url(self):
        url = reverse('workout-detail', args=[self.workout.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
