from dynamic_rest.serializers import (
  DynamicModelSerializer,
)


class AddCreatorSerializerMixin(object):
  CREATOR_FIELD = 'creator'

  def to_internal_value(self, data):
    request = self.context.get('request')
    user = request.user if request else None
    if self.CREATOR_FIELD and not data.get(self.CREATOR_FIELD):
      data[self.CREATOR_FIELD] = user.pk
    return super().to_internal_value(data)


class BaseSerializer(AddCreatorSerializerMixin, DynamicModelSerializer):
   pass 
