from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from bbook_backend.api.serializers import UserSerializer


class UserViewSet(BaseViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk and (pk == 'me'):
            self.kwargs['pk'] = request.user.id

        return super(UserViewSet, self).retrieve(request, *args, **kwargs)
