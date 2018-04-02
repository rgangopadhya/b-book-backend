from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from bbook_backend.models import Character
from bbook_backend.api.serializers import CharacterSerializer


class CharacterViewSet(BaseViewSet):
    model = Character
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = (IsAuthenticated,)
