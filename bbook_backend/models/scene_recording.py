from django.db import models
from .base import Model
from .story import Story
from .scene import Scene
from bbook_backend.storage_backends import SceneRecordingStorage


class SceneRecording(Model):

    class Meta:
        app_label = 'bbook_backend'

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='recordings',
    )
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name='recordings',
        default=None,
    )
    order = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    recording = models.FileField(storage=SceneRecordingStorage())
    duration = models.FloatField(null=True, blank=True)
