from django.core.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def make_token_for_user(sender, **kwargs):
  user = kwargs.get('instance')

  if not user:
    return

  Token.objects.get_or_create(user=user)

