from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from bbook_backend.models import SceneRecording
from bbook_backend.api.serializers import SceneRecordingSerializer


class SceneRecordingViewSet(BaseViewSet):
    model = SceneRecording
    queryset = SceneRecording.objects.all()
    serializer_class = SceneRecordingSerializer
    permission_classes = (IsAuthenticated,)
