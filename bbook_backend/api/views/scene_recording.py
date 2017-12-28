from rest_framework.permissions import IsAuthenticated
from dynamic_rest.viewsets import DynamicModelViewSet
from bbook_backend.models import SceneRecording
from bbook_backend.api.serializers import SceneRecordingSerializer


class SceneRecordingViewSet(DynamicModelViewSet):
  model = SceneRecording
  queryset = SceneRecording.objects.all()
  serializer_class = SceneRecordingSerializer
  permission_classes = (IsAuthenticated,)
