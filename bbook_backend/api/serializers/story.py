from dynamic_rest.serializers import (
  DynamicRelationField,
)
from .base import BaseSerializer
from bbook_backend.models import Story


class StorySerializer(BaseSerializer):

  class Meta:
    model = Story
    name = 'story'
    plural_name = 'stories'
    fields = (
      'creator',
      'created_at',
      'recordings',
    )

  recordings = DynamicRelationField(
    'bbook_backend.api.serializers.SceneRecordingSerializer',
    many=True,
  )
