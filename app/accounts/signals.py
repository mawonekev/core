import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .emails import send_verification_email

User = get_user_model()
logger = logging.getLogger('app.accounts')


@receiver(post_save, sender=User)
def send_verification_on_registration(sender, instance, created, **kwargs):
    """Send verification email when user is created"""
    if created:
        # Update verification sent timestamp
        instance.email_verification_sent_at = timezone.now()
        instance.save(update_fields=['email_verification_sent_at'])

        # Send verification email
        logger.info(f"New user registered: {instance.username} ({instance.email})")
        send_verification_email(instance)
