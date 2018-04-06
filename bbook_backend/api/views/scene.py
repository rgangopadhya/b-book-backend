from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from bbook_backend.models import Scene
from bbook_backend.api.serializers import SceneSerializer


class SceneViewSet(BaseViewSet):
    model = Scene
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        random_page_size = int(self.request.query_params.get('random', 0))
        if random_page_size:
            queryset = queryset.order_by('?')[:random_page_size]
        return queryset
