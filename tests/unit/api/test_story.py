from django.test import TestCase
from django.contrib.auth.models import User
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from moto import mock_s3
from bbook_backend.models import (
    SceneRecording,
    Story,
)
from tests.unit.fixtures import StoryFixture


class StoryAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        self.fixture = StoryFixture()
        self.other_user = User.objects.create(username='other')
        self.other_story = Story.objects.create(creator=self.other_user)

    def tearDown(self):
        self.mock_s3.stop()

    def test_can_list_stories(self):
        self.fixture.login_user(self.client)
        response = self.client.get('/v0/stories/?include[]=recordings.')
        self.assertEqual(response.status_code, 200)
        data = response.json()['stories']
        self.assertEqual(len(data), 1)
        story = data[0]
        self.assertIsNone(story['cover_image'])

    def test_can_retrieve_own_story(self):
        self.fixture.login_user(self.client)
        response = self.client.get('/v0/stories/%s/' % self.fixture.story.pk)
        self.assertEqual(response.status_code, 200)

    def test_cant_retrieve_other_user_stories(self):
        self.fixture.login_user(self.client)
        response = self.client.get('/v0/stories/%s/' % self.other_story.pk)
        self.assertEqual(response.status_code, 404)

    def test_get_cover_image(self):
        # now add a recording
        self.fixture.login_user(self.client)
        recording = SimpleUploadedFile('recording.mp3', b'yep')
        SceneRecording.objects.create(
            recording=recording,
            story=self.fixture.story,
            scene=self.fixture.scene1,
        )
        response = self.client.get('/v0/stories/?include[]=recordings.')
        self.assertEqual(response.status_code, 200)
        data = response.json()['stories']
        self.assertEqual(len(data), 1)
        story = data[0]
        self.assertIn(
            self.fixture.scene1.image.file.name,
            story['cover_image']
        )

    def test_can_save_single_recording(self):
        self.fixture.login_user(self.client)
        recording = SimpleUploadedFile('recording1.mp3', b'yep')
        scenes = [self.fixture.scene1.pk, self.fixture.scene2.pk]
        response = self.client.post(
            '/v0/stories/',
            {
                'character': self.fixture.character.pk,
                'durations': json.dumps([
                    {'scene': self.fixture.scene2.pk, 'duration': 4.0},
                    {'scene': self.fixture.scene1.pk, 'duration': 5.2},
                ]),
                'scene_order': ','.join(map(str, scenes)),
                'recording': recording,
            }
        )
        self.assertEqual(
            response.status_code,
            201,
            '%s: %s' % (response.status_code, response.content),
        )
        data = response.json()['story']
        self.assertEqual(set(data['scenes']), set(scenes))
        # checks that the first scene is set correctly
        self.assertIn(self.fixture.scene2.image.name, data['cover_image'])

    def test_can_save_title(self):
        self.assertIsNone(self.fixture.story.title.name)
        title = SimpleUploadedFile('title.mp3', b'yep')
        self.fixture.login_user(self.client)
        response = self.client.patch(
            '/v0/stories/%s/' % self.fixture.story.pk,
            data={'title': title},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        story = Story.objects.get(pk=self.fixture.story.pk)
        self.assertIsNotNone(story.title.name)


class StoryRecordingAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        self.fixture = StoryFixture()

    def tearDown(self):
        self.mock_s3.stop()

    def test_story_recording_post(self):
        self.client.login(username='admin', password='blah')
        recording1 = SimpleUploadedFile('recording1.mp3', b'yep')
        recording2 = SimpleUploadedFile('recording2.mp3', b'yephah')
        expected_order = [self.fixture.scene1.pk, self.fixture.scene2.pk]
        expected_durations = [100, 300]
        data = {
                self.fixture.scene1.pk: recording1,
                self.fixture.scene2.pk: recording2,
                'scene_order': ','.join(map(str, expected_order)),
                'durations': ','.join(map(str, expected_durations)),
                'character': self.fixture.character.pk,
        }
        response = self.client.post(
            '/v0/story_recordings/', data
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()['story_recording']
        recordings = data['recordings']
        self.assertEqual(len(recordings), 2)
        self.assertIsNotNone(data['story'])
