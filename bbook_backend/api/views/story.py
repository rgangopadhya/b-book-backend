from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from django.db import transaction
from bbook_backend.models import (
  Scene,
  Story,
)
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from bbook_backend.api.serializers import (
  SceneRecordingSerializer,
  StorySerializer,
  StoryRecordingSerializer,
)
from bbook_backend.api.serializers.story import (
  _StoryRecording,
)


class StoryViewSet(BaseViewSet):
  model = Story
  queryset = Story.objects.all()
  serializer_class = StorySerializer
  permission_classes = (IsAuthenticated,)


class StoryRecordingViewSet(BaseViewSet):
  """
  multipart/form-data
  {
    scene_id1: recording1,
    scene_id2: recording2,
    scene_order: [scene_id1, scene_id2],
    ...
  }
  """
  serializer_class = StoryRecordingSerializer
  permission_classes = (IsAuthenticated,)

  def _create_scene_recordings(self, request, story):
    try:
      scene_order = request.data.getlist('scene_order')
    except KeyError:
      raise Exception('orders key required')

    result = []
    for scene_id in scene_order:
      recording = request.data[scene_id]
      serializer = SceneRecordingSerializer(data={
        'story': story.pk,
        'scene': scene_id,
        'recording': recording,
      })
      serializer.is_valid(raise_exception=True)
      result.append(serializer.save())
    return result

  @transaction.atomic
  def create(self, request, *args, **kwargs):
    user = request.user
    story = Story.objects.create(creator=user)
    recordings = self._create_scene_recordings(request, story)
    story_recording = _StoryRecording(user, recordings, story)
    serializer = self.get_serializer(story_recording)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
