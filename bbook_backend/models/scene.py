from django.db import models
from django.contrib.auth.models import User
from .base import Model
from bbook_backend.storage_backends import SceneStorage


class Scene(Model):

    class Meta:
        app_label = 'bbook_backend'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(storage=SceneStorage())
