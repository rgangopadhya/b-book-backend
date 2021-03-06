import json
from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from django.db import transaction
from bbook_backend.models import (
    Story,
)
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

    def filter_queryset(self, queryset):
        user = self.request.user
        return super().filter_queryset(queryset).filter(
            creator=user
        )

    def create(self, request, *args, **kwargs):
        # implement CreateViewMixin.create since we need to
        # hack around the fact that we cant pass dict/list
        # in multipart/form (may be able to do this with a custom)
        # parser -- look into
        data = request.data
        modified_data = {
            'character': data['character'],
            'scene_durations': json.loads(data['durations']),
            'scenes': list(map(int, data['scene_order'].split(','))),
            'recording': data['recording']
        }
        serializer = self.get_serializer(data=modified_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class StoryRecordingViewSet(BaseViewSet):
    """
    multipart/form-data
    {
        scene_id1: recording1,
        scene_id2: recording2,
        scene_order: [scene_id1, scene_id2],
        durations: [],
        character: character_pk
        ...
    }
    """
    serializer_class = StoryRecordingSerializer
    permission_classes = (IsAuthenticated,)

    def _create_scene_recordings(self, request, story):
        try:
            scene_order = request.data.get('scene_order').split(',')
            durations = request.data.get('durations').split(',')
        except KeyError:
            raise Exception('scene_order key required')
        if len(scene_order) == 0 or len(durations) == 0:
            raise Exception('No durations or scene_order')

        result = []
        for i, (scene_id, duration) in enumerate(zip(scene_order, durations)):
            try:
                recording = request.data[scene_id]
            except Exception as error:
                print('MultiValue', request.data, scene_id)
                raise error
            serializer = SceneRecordingSerializer(data={
                'story': story.pk,
                'scene': scene_id,
                'order': i,
                'recording': recording,
                'duration': duration
            })
            serializer.is_valid(raise_exception=True)
            result.append(serializer.save())
        return result

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        story = Story.objects.create(
            creator=user,
            character_id=request.data['character'],
        )
        recordings = self._create_scene_recordings(request, story)
        story_recording = _StoryRecording(user, recordings, story)
        serializer = self.get_serializer(story_recording)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
