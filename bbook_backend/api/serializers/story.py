from dynamic_rest.serializers import (
    DynamicRelationField,
    DynamicEphemeralSerializer,
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
            'character',
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
    character = DynamicRelationField(
        'bbook_backend.api.serializers.CharacterSerializer',
        required=True,
    )
    cover_image = DynamicMethodField(
        requires=['recordings.scene.']
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
        except Exception as e:
            print('Failed', e)

        return FileField().to_representation(image)

    def get_duration(self, instance):
        try:
            return sum([r.duration for r in instance.recordings.all()])
        except Exception as e:
            print('Failed', e)


class _StoryRecording():

    def __init__(self, user, recordings, story):
        self.creator = user
        self.recordings = recordings
        self.story = story


class StoryRecordingSerializer(DynamicEphemeralSerializer):

    class Meta:
        name = 'story_recording'
        fields = (
            'creator',
            'story',
            'recordings',
        )

    creator = DynamicRelationField(
        'bbook_backend.api.serializers.UserSerializer',
        required=False,
    )
    recordings = DynamicRelationField(
        'bbook_backend.api.serializers.SceneRecordingSerializer',
        many=True,
    )
    story = DynamicRelationField(
        'bbook_backend.api.serializers.StorySerializer',
        required=False,
    )
