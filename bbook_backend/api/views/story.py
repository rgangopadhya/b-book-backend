from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
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
    ...
  }
  """
  serializer_class = StoryRecordingSerializer
  permission_classes = (IsAuthenticated,)

  def create(self, *args, **kwargs):
    data = []
    user = self.request.user
    story = Story.objects.create(creator=user)
    for scene_id in self.request.data.keys():
      recording = self.request.data[scene_id]
      serializer = SceneRecordingSerializer(data={
        'story': story.pk,
        'scene': scene_id,
        'recording': recording
      })
      serializer.is_valid(raise_exception=True)
      data.append(serializer.save())
    story_recording = _StoryRecording(user, data, story)
    serializer = StoryRecordingSerializer(story_recording)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
