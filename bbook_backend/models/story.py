from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from bbook_backend.storage_backends import (
    StoryStorage,
    StoryTitleStorage,
)
from .base import Model
from .character import Character
from .scene import Scene


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
    scenes = models.ManyToManyField(
        Scene,
        related_name='stories',
    )
    scene_durations = JSONField(
        null=True,
        blank=True,
    )
    recording = models.FileField(
        storage=StoryStorage(),
        null=True,
        blank=True,
    )
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
