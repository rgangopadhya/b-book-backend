from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .base import BaseViewSet
from bbook_backend.api.serializers import UserSerializer


class UserViewSet(BaseViewSet):
  model = User
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (IsAuthenticated,)

