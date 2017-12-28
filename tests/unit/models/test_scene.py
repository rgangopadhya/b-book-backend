from bbook_backend.models import Scene
from django.test import TestCase

class SceneTestCase(TestCase):
    def test_ok(self):
        self.assertTrue(
            Scene.objects.create().pk is not None
        )