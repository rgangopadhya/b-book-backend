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
            'recording',
            'recordings',
            'scenes',
            'scene_durations',
            'title',
        )

    recording = FileField()
    recordings = DynamicRelationField(
        'bbook_backend.api.serializers.SceneRecordingSerializer',
        many=True,
    )
    scenes = DynamicRelationField(
        'bbook_backend.api.serializers.SceneSerializer',
        many=True,
    )
    character = DynamicRelationField(
        'bbook_backend.api.serializers.CharacterSerializer',
        required=True,
    )
    cover_image = DynamicMethodField(
        requires=['recordings.scene.', 'scenes.']
    )
    duration = DynamicMethodField(
        requires=['recordings.']
    )
    title = FileField(required=False)

    def get_cover_image(self, instance):
        image = None
        try:
            if instance.scene_durations is not None:
                scene_id = instance.scene_durations[0]['scene']
                # take advantage of prefetching
                image = next(
                    scene.image for scene in instance.scenes.all()
                    if scene.id == scene_id
                )
            else:
                image = min(
                    instance.recordings.all(), key=lambda rec: rec.order
                ).scene.image
        except Exception as e:
            print('get_cover_image failed', e)

        return FileField().to_representation(image)

    def get_duration(self, instance):
        try:
            if instance.recording is not None:
                return sum([
                    r['duration'] for r in instance.scene_durations
                ])
            return sum([r.duration for r in instance.recordings.all()])
        except Exception as e:
            print('get_duration failed', e)


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
