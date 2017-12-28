from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from bbook_backend.models import Story
from rest_framework.decorators import list_route
from rest_framework.response import Response
from bbook_backend.api.serializers import (
  StorySerializer,
  SceneRecordingSerializer,
)


class StoryViewSet(BaseViewSet):
  model = Story
  queryset = Story.objects.all()
  serializer_class = StorySerializer
  permission_classes = (IsAuthenticated,)

  @list_route(methods=['post'])
  def make_story(self, request):
    # parse the request payload manually
    creator = request.user
    payload = request.POST
    scene_recordings = payload.scene_recordings
    story = Story.objects.create(
      creator=creator,
    )
    for sr in scene_recordings:
      data = sr
      data.update({
        'story': story.pk,
      });
      serializer = SceneRecordingSerializer(data=data)
      serializer.is_valid(raise_exception=True)
      serializer.save()

    story_serializer = StorySerializer(story)
    return Response(story_serializer.data)
