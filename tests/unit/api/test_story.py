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
    self.scene = Scene.objects.create(
      creator=self.admin,
      image=self.scene_image
    )
    self.story = Story.objects.create(creator=self.admin)

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

  def test_get_cover_image(self):
    # now add a recording
    self.client.login(username='admin', password='blah')
    recording = SimpleUploadedFile('recording.mp3', b'yep')
    sr = SceneRecording.objects.create(
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
