from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from moto import mock_s3
import boto3
from bbook_backend.models import (
    Scene,
    Story,
)


class SceneRecordingAPITestCase(TestCase):

    @mock_s3
    def setUp(self):
        self.client = Client()
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='b-book-test')
        self.scene_image = SimpleUploadedFile('test.jpg', b'wooo')
        self.admin = User.objects.create(username='admin')
        self.admin.set_password('blah')
        self.admin.save()
        self.scene = Scene.objects.create(
            creator=self.admin,
            image=self.scene_image,
        )
        self.story = Story.objects.create(creator=self.admin)

    @mock_s3
    def test_can_save_recording(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='b-book-test')
        self.client.login(username='admin', password='blah')
        recording = SimpleUploadedFile('recording.mp3', b'yep')
        response = self.client.post('/v0/scene_recordings/', {
            'scene': self.scene.pk,
            'story': self.story.pk,
            'recording': recording,
            'order': 0
        })
        self.assertEqual(response.status_code, 201)
        data = response.json()['scene_recording']
        self.assertIsNotNone(data['recording'])
