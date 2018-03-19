import os
from django.contrib.auth.models import User
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.core.files import File
from bbook_backend.models import Scene


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--username', action='store')
        parser.add_argument('--directory', action='store')

    def handle(self, *args, **options):
        username = options.get('username')
        directory = options.get('directory')
        print('=== Got username %s, directory %s' % (username, directory))
        if not username:
            raise CommandError('Please provide a username')
        if not directory:
            raise CommandError('Please provide a directory')

        user = User.objects.get(username=username)

        for filename in os.listdir(directory):
            if '.png' not in filename:
                continue
            print('== About to open %s' % filename)
            with open(os.path.join(directory, filename), 'rb') as fp:
                file = File(fp)
                Scene.objects.get_or_create(
                    image=file,
                    creator=user,
                )
