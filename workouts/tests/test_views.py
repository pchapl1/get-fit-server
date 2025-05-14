from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from workouts.models import Workout
from datetime import timedelta

class WorkoutViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.workout = Workout.objects.create(
            user=self.user,
            name='Morning Workout',
            type='Cardio',
            duration=timedelta(minutes=30)
        )
        self.list_url = reverse('workout-list')
        self.detail_url = reverse('workout-detail', args=[self.workout.id])

    def test_list_workouts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Morning Workout')

    def test_retrieve_workout(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.workout.id)
        self.assertEqual(response.data['name'], 'Morning Workout')

    def test_create_workout(self):
        data = {
            "user": self.user.id,
            "name": "Evening Session",
            "type": "HIIT",
            "duration": "00:45:00"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 2)
        self.assertEqual(Workout.objects.latest('id').name, 'Evening Session')

    def test_update_workout(self):
        data = {
            "user": self.user.id,
            "name": "Updated Workout",
            "type": "Strength",
            "duration": "01:00:00"
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workout.refresh_from_db()
        self.assertEqual(self.workout.name, "Updated Workout")
        self.assertEqual(self.workout.type, "Strength")

    def test_delete_workout(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Workout.objects.count(), 0)

    def test_invalid_create_workout(self):
        # Missing 'name' and 'type'
        data = {
            "user": self.user.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('type', response.data)
