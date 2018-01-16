from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class RegistrationAPITestCase(TestCase):

  def setUp(self):
    self.client = Client()

  def test_can_create_new_user(self):
    data = {
      'username': 'woo',
      'email': 'woo@gmail.com',
      'password1': 'blahblah',
      'password2': 'blahblah'
    }
    response = self.client.post('/rest-auth/registration/', data)
    self.assertEqual(response.status_code, 201)
    body = response.json()
    self.assertIn('key', body)
