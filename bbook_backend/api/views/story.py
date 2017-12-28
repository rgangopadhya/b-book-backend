from rest_framework.permissions import IsAuthenticated
from dynamic_rest.viewsets import DynamicModelViewSet
from bbook_backend.models import Story
from bbook_backend.api.serializers import StorySerializer


class StoryViewSet(DynamicModelViewSet):
  model = Story
  queryset = Story.objects.all()
  serializer_class = StorySerializer
  permission_classes = (IsAuthenticated,)
