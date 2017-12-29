from dynamic_rest.serializers import (
  DynamicModelSerializer,
)


class BaseSerializer(DynamicModelSerializer):
    
    def to_internal_value(self, data):
      request = self.context.get('request')
      user = request.user if request else None
      if not data.get('creator'):
        data['creator'] = user.pk
      return super().to_internal_value(data)
