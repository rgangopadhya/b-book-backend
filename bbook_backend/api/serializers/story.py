from dynamic_rest.serializers import (
  DynamicRelationField,
)
from dynamic_rest.fields import (
  DynamicMethodField,
)
from rest_framework.serializers import FileField
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
      'cover_image',
      'duration',
      'id',
      'recordings',
    )

  recordings = DynamicRelationField(
    'bbook_backend.api.serializers.SceneRecordingSerializer',
    many=True,
  )

  cover_image = DynamicMethodField(
    requires=['recordings.']
  )
  duration = DynamicMethodField(
    requires=['recordings.']
  )

  def get_cover_image(self, instance):
    image = None
    try:
      image = min(
        instance.recordings.all(), key=lambda rec: rec.order
      ).scene.image
    except:
      pass

    return FileField().to_representation(image)

  def get_duration(self, instance):
    try:
      return sum([r.duration for r in instance.recordings.all()])
    except:
      pass
