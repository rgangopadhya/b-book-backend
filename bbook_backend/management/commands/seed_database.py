from django.contrib.auth.models import User
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.core.files import File
from bbook_backend.models import Scene


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            action='store',
        )
        parser.add_argument(
            '--username',
            action='store',
        )

    def handle(self, *args, **options):
        password = options.get('password')
        username = options.get('username')
        if not password or not username:
            raise CommandError('No password or username supplied')

        admin, new = User.objects.get_or_create(
            username=username
        )
        if new:
            print('== Created user %s' % username)
            admin.set_password(password)
            admin.save()
        else:
            print('== User already exists ==')

        # create 5 scenes
        for i in range(5):
            filename = 'bbook_backend/static/%s.jpg' % (i + 1)
            print('About to do %s' % filename)
            # make the s3 file
            with open(filename, 'rb') as fp:
                file = File(fp)
                Scene.objects.get_or_create(
                    image=file,
                    creator=admin,
                )
