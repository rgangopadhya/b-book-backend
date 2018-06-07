from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from moto import mock_s3
from tests.unit.fixtures import StoryFixture


class SceneRecordingAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        self.fixture = StoryFixture()

    def tearDown(self):
        self.mock_s3.stop()

    def test_can_save_recording(self):
        self.fixture.login_user(self.client)
        recording = SimpleUploadedFile('recording.mp3', b'yep')
        response = self.client.post('/v0/scene_recordings/', {
            'scene': self.fixture.scene1.pk,
            'story': self.fixture.story.pk,
            'recording': recording,
            'order': 0
        }, format='multipart')
        self.assertEqual(response.status_code, 201)
        data = response.json()['scene_recording']
        self.assertIsNotNone(data['recording'])
