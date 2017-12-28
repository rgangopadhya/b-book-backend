from bbook_backend.models import SceneRecording
from django.test import TestCase

class SceneRecordingTestCase(TestCase):
    def test_ok(self):
        self.assertTrue(
            SceneRecording.objects.create().pk is not None
        )