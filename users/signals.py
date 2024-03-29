from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_account(sender, instance=None, created=False, **kwargs):
    if created:
        # generate the token for user
        Token.objects.create(user=instance)
