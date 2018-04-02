from rest_framework.serializers import FileField
from dynamic_rest.serializers import (
    DynamicRelationField,
)
from .base import BaseSerializer
from bbook_backend.models import Character


class CharacterSerializer(BaseSerializer):

    class Meta:
        model = Character
        name = 'character'
        fields = (
            'creator',
            'created_at',
            'id',
            'image',
            'name',
        )

    creator = DynamicRelationField(
        'bbook_backend.api.serializers.UserSerializer',
    )
    image = FileField()
