from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from bbook_backend.models import Scene
from bbook_backend.api.serializers import SceneSerializer


class SceneViewSet(BaseViewSet):
    model = Scene
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    permission_classes = (IsAuthenticated,)
