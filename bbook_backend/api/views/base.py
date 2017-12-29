from dynamic_rest.viewsets import DynamicModelViewSet


class AddCreatorMixin(object):

  def create(self, request):
    creator = request.user
    data = request.data
    if not data.get('creator'):
      data['creator'] = creator.pk
    return super().create(request)


class BaseViewSet(AddCreatorMixin, DynamicModelViewSet):
  pass
