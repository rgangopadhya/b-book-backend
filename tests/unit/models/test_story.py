from bbook_backend.models import Story
from django.test import TestCase

class StoryTestCase(TestCase):
    def test_ok(self):
        self.assertTrue(
            Story.objects.create().pk is not None
        )