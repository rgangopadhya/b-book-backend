from rest_framework.permissions import IsAuthenticated
from dynamic_rest.viewsets import DynamicModelViewSet
from bbook_backend.models import Scene
from bbook_backend.api.serializers import SceneSerializer


class SceneViewSet(DynamicModelViewSet):
  model = Scene
  queryset = Scene.objects.all()
  serializer_class = SceneSerializer
  permission_classes = (IsAuthenticated,)
