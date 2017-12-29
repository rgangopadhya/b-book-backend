"""bbook_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/2.0/topics/http/urls/

The `djx.urls:load_urls` utility is used to automatically include all
url patterns from `urls.py` modules in project subdirectories.

For example, `bbook_backend.api.urls:urlpatterns` will be routed
under the "/api" prefix.
"""

from django.conf.urls import (
    include,
    url,
)
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from djx.urls import load_urls
from inspect import isclass
from dynamic_rest.routers import DynamicRouter
from bbook_backend.api import views
from bbook_backend.api.views.auth_views import BBookLoginView
from rest_framework.authtoken import views as authtoken_views


urlpatterns = []
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r'^admin/', admin.site.urls)
    )


router = DynamicRouter()


def register_views(views):
    for name in dir(views):
        view = getattr(views, name)
        if (
            isclass(view) and
            getattr(view, 'serializer_class', None) and
            getattr(view, 'IS_CANONICAL', True)
        ):
          router.register_resource(view, namespace='v0')


register_views(views)


urlpatterns.extend([
    url(r'^', include(router.urls)),
    path('accounts/login/', BBookLoginView.as_view(), name='login'),
    url(r'^api-token-auth/', authtoken_views.obtain_auth_token),
])
