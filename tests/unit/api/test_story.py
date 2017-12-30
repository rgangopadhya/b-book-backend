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


class StoryAPITestCase(TestCase):

  def setUp(self):
    self.client = Client()
    self.admin = User.objects.create(username='admin')
    self.admin.set_password('blah')
    self.admin.save()
    self.story = Story.objects.create(creator=self.admin)

  def test_can_list_stories(self):
    self.client.login(username='admin', password='blah')
    response = self.client.get('/v0/stories/?include[]=recordings.')
    self.assertEqual(response.status_code, 200)
    data = response.json()['stories']
    self.assertEqual(len(data), 1)
