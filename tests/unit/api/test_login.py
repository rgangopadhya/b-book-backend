from django.test import TestCase
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

        # then use this key in auth login
        response = self.client.get(
            '/v0/users/me/',
            {},
            Authorization='Token %s' % body['key']
        )
        self.assertEqual(response.status_code, 200)

        # logout
        response = self.client.post('/rest-auth/logout/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api-token-auth/', {
            'username': 'woo',
            'password': 'blahblah'
        })
        self.assertEqual(response.status_code, 200)
