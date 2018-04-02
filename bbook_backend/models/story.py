from django.db import models
from django.contrib.auth.models import User
from .base import Model
from .character import Character


class Story(Model):

    class Meta:
        app_label = 'bbook_backend'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
