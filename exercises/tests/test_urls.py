from django.test import SimpleTestCase
from django.urls import reverse, resolve
from exercises.views import ExerciseViewSet


class ExerciseURLsTest(SimpleTestCase):

    def test_exercise_list_url_resolves(self):
        url = reverse('exercise-list')
        self.assertEqual(url, '/api/exercises/')  # full path including api prefix and trailing slash

    def test_exercise_detail_url_resolves(self):
        url = reverse('exercise-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/api/exercises/1/')  # full path including api prefix and trailing slash

    def test_exercise_list_url_resolves_to_viewset(self):
        url = reverse('exercise-list')
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ExerciseViewSet)

    def test_exercise_detail_url_resolves_to_viewset(self):
        url = reverse('exercise-detail', kwargs={'pk': 1})
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ExerciseViewSet)
