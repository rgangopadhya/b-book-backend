from dynamic_rest.viewsets import DynamicModelViewSet


class AddCreatorMixin(object):

  def create(self, request):
    creator = request.user
    request.data = request.data.copy()
    if not request.data.get('creator'):
      request.data['creator'] = creator.pk
    return super().create(request)


class BaseViewSet(AddCreatorMixin, DynamicModelViewSet):
  pass
