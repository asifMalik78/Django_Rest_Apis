from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Customer


@receiver(post_save , sender=settings.AUTH_USER_MODEL)
def create_custom_for_new_user(sender , **kwargs):
    created = kwargs.get('created')
    isinstance = kwargs.get('instance')
    if created:
        Customer.objects.create(user=isinstance)