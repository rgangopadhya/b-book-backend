from django.contrib.auth.models import User
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.core.files import File
from bbook_backend.models import Character


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--username', action='store')
        parser.add_argument('--image', action='store')
        parser.add_argument('--name', action='store')

    def handle(self, *args, **options):
        username = options.get('username')
        image_name = options.get('image')
        character_name = options.get('name')
        if not username:
            raise CommandError('Please provide username')
        if not image_name:
            raise CommandError('Please provide image')
        if not character_name:
            raise CommandError('Please provide name')

        user = User.objects.get(username=username)
        with open(image_name, 'rb') as fp:
            file = File(fp)
            character, new = Character.objects.get_or_create(
                name=character_name,
                creator=user,
                defaults={
                    'image': file
                }
            )
            if not new:
                print('=== Not a new character ===')
