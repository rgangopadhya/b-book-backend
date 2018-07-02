import boto3
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from bbook_backend.models import (
    Character,
    Scene,
    Story,
)


class StoryFixture():

    def __init__(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='b-book-test')
        self.make_user()
        self.make_story()

    def make_story(self):
        self.make_character()
        self.scene_image1 = SimpleUploadedFile('test1.jpg', b'wooo')
        self.scene_image2 = SimpleUploadedFile('test2.jpg', b'wooo')
        self.scene1 = Scene.objects.create(
            creator=self.user,
            image=self.scene_image1,
            character=self.character,
        )
        self.scene2 = Scene.objects.create(
            creator=self.user,
            image=self.scene_image2,
            character=self.character,
        )
        self.story = Story.objects.create(
            creator=self.user,
            character=self.character,
        )

    def make_user(self):
        self.password = 'blah'
        self.username = 'admin'
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def login_user(self, client):
        client.login(
            username=self.username,
            password=self.password,
        )

    def make_character(self):
        self.char_image = SimpleUploadedFile('t2.jpg', b'hax')
        self.character = Character.objects.create(
            name='harry',
            creator=self.user,
            image=self.char_image,
        )
