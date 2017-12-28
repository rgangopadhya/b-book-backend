from rest_framework.serializers import FileField
from dynamic_rest.serializers import (
  DynamicRelationField,
)
from .base import BaseSerializer
from bbook_backend.models import Scene


class SceneSerializer(BaseSerializer):

  class Meta:
    model = Scene
    name = 'scene'
    fields = (
      'creator',
      'created_at',
      'id',
      'image',
    )

  creator = DynamicRelationField(
    'bbook_backend.api.serializers.UserSerializer',
  )

  image = FileField()
