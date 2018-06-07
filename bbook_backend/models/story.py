from django.db import models
from django.contrib.auth.models import User
from bbook_backend.storage_backends import StoryTitleStorage
from .base import Model
from .character import Character


class Story(Model):

    class Meta:
        app_label = 'bbook_backend'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.FileField(
        storage=StoryTitleStorage(),
        null=True,
        blank=True,
    )
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
