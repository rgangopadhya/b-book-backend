from rest_framework.serializers import FileField
from dynamic_rest.serializers import (
  DynamicRelationField,
)
from .base import BaseSerializer
from bbook_backend.models import (
  SceneRecording,
)


class SceneRecordingSerializer(BaseSerializer):

  class Meta:
    model = SceneRecording
    name = 'scene_recording'
    fields = (
      'created_at',
      'id',
      'recording',
      'scene',
      'story',
    )

  scene = DynamicRelationField(
    'bbook_backend.api.serializers.SceneSerializer',
  )
  story = DynamicRelationField(
    'bbook_backend.api.serializers.StorySerializer',
  )
  recording = FileField()
