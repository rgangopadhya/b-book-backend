from django.test import TestCase
from rest_framework.test import APIClient
from moto import mock_s3
from tests.unit.fixtures import StoryFixture


class SceneAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        self.fixture = StoryFixture()

    def tearDown(self):
        self.mock_s3.stop()

    # def test_can_filter_scenes_by_character(self):
    #     self.fixture.login_user(self.client)
    #     response = self.client.get(
    #         '/v0/scenes/?filter{character}=%s' % self.fixture.character.pk
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     data = response.json()['scenes']
    #     self.assertEqual(len(data), 2)

    def test_can_retrieve_random_page(self):
        self.fixture.login_user(self.client)
        id = self.fixture.character.id
        response = self.client.get(
            '/v0/scenes/?random=1&filter{character}=%s' % id
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()['scenes']
        self.assertEqual(len(data), 1)
