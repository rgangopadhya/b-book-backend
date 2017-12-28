from django.contrib.auth.models import User
from dynamic_rest.serializers import (
  DynamicModelSerializer,
)


class UserSerializer(DynamicModelSerializer):

  class Meta:
    model = User
    name = 'user'
    fields = (
      'id',
      'first_name',
      'last_name',
      'username',
      'email',
    )

