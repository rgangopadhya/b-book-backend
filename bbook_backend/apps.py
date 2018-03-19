from __future__ import unicode_literals

from django.apps import AppConfig as _AppConfig


class AppConfig(_AppConfig):
    name = 'bbook_backend'

    def ready(self):
        import bbook_backend.signals  # noqa
        super().ready()
