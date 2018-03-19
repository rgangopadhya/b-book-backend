from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from moto import mock_s3
import boto3
from bbook_backend.models import (
    Scene,
    SceneRecording,
    Story,
)


class StoryAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='b-book-test')
        self.scene_image = SimpleUploadedFile('test.jpg', b'wooo')
        self.admin = User.objects.create(username='admin')
        self.admin.set_password('blah')
        self.admin.save()
        self.other_user = User.objects.create(username='other')
        self.scene = Scene.objects.create(
            creator=self.admin,
            image=self.scene_image
        )
        self.story = Story.objects.create(creator=self.admin)
        self.other_story = Story.objects.create(creator=self.other_user)

    def tearDown(self):
        self.mock_s3.stop()

    def test_can_list_stories(self):
        self.client.login(username='admin', password='blah')
        response = self.client.get('/v0/stories/?include[]=recordings.')
        self.assertEqual(response.status_code, 200)
        data = response.json()['stories']
        self.assertEqual(len(data), 1)
        story = data[0]
        self.assertIsNone(story['cover_image'])

    def test_can_retrieve_own_story(self):
        self.client.login(username='admin', password='blah')
        response = self.client.get('/v0/stories/%s/' % self.story.pk)
        self.assertEqual(response.status_code, 200)

    def test_cant_retrieve_other_user_stories(self):
        self.client.login(username='admin', password='blah')
        response = self.client.get('/v0/stories/%s/' % self.other_story.pk)
        self.assertEqual(response.status_code, 404)

    def test_get_cover_image(self):
        # now add a recording
        self.client.login(username='admin', password='blah')
        recording = SimpleUploadedFile('recording.mp3', b'yep')
        SceneRecording.objects.create(
            recording=recording,
            story=self.story,
            scene=self.scene,
        )
        response = self.client.get('/v0/stories/?include[]=recordings.')
        self.assertEqual(response.status_code, 200)
        data = response.json()['stories']
        self.assertEqual(len(data), 1)
        story = data[0]
        self.assertIn(self.scene.image.file.name, story['cover_image'])


class StoryRecordingAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='b-book-test')
        self.scene_image1 = SimpleUploadedFile('test.jpg', b'wooo')
        self.scene_image2 = SimpleUploadedFile('test2.jpg', b'blahhh')
        self.admin = User.objects.create(username='admin')
        self.admin.set_password('blah')
        self.admin.save()
        self.scene1 = Scene.objects.create(
            creator=self.admin,
            image=self.scene_image1
        )
        self.scene2 = Scene.objects.create(
            creator=self.admin,
            image=self.scene_image2
        )

    def test_story_recording_post(self):
        self.client.login(username='admin', password='blah')
        recording1 = SimpleUploadedFile('recording1.mp3', b'yep')
        recording2 = SimpleUploadedFile('recording2.mp3', b'yephah')
        expected_order = [self.scene1.pk, self.scene2.pk]
        expected_durations = [100, 300]
        data = {
                self.scene1.pk: recording1,
                self.scene2.pk: recording2,
                'scene_order': ','.join(map(str, expected_order)),
                'durations': ','.join(map(str, expected_durations))
        }
        response = self.client.post(
            '/v0/story_recordings/', data
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()['story_recording']
        recordings = data['recordings']
        self.assertEqual(len(recordings), 2)
        self.assertIsNotNone(data['story'])
        self.assertEqual(expected_order, recordings)
