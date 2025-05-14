from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from workouts.models import Exercise, Workout, WorkoutExercise


class ExerciseAPITestCase(APITestCase):

    def setUp(self):
        self.exercise = Exercise.objects.create(
            name="Bench Press",
            category="Push",
            muscles_targeted="Chest",   
            duration=None
        )

        self.detail_url = reverse('exercise-detail', kwargs={'pk': self.exercise.id})
        self.list_url = reverse('exercise-list')  

    def test_create_exercise(self):
        data = {
            "name": "Squat",
            "category": "Legs",
            "muscles_targeted": "Quads",
            "duration": None
        }
        response = self.client.post(self.list_url, data, format='json')
        print('TEST CREATE: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Squat')

    def test_read_exercise_list(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Bench Press")


    def test_get_single_exercise(self):
        response = self.client.get(self.detail_url)

        # assert status is ok
        self.assertEqual(response.status_code, 200)

        # assert the response contains correct data
        self.assertEqual(response.data['id'], self.exercise.id)
        self.assertEqual(response.data['name'], self.exercise.name)
        self.assertEqual(response.data['category'], self.exercise.category)
        self.assertEqual(response.data['muscles_targeted'], self.exercise.muscles_targeted)
        self.assertEqual(response.data['duration'], self.exercise.duration)

    def test_update_exercise(self):
        data = {
            "name": "Incline Bench Press",
            "category": "Push",
            "muscles_targeted": "Upper Chest",
            "duration": None
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.name, "Incline Bench Press")


    def test_partial_update_exercise(self):
        response = self.client.patch(self.detail_url, {"name": "Close Grip Bench"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.name, "Close Grip Bench")
    

    def test_delete_exercise(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exercise.objects.count(), 0)
