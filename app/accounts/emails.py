import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger('app.accounts')


def send_verification_email(user, request=None):
    try:
        frontend_url = getattr(settings, 'FRONTEND_URL', 'https://xenohuru.cleven.is-a.dev')
        verification_url = f"{frontend_url}/verify-email/?token={user.email_verification_token}"

        message = f"""Welcome to Xenohuru, {user.username}!

Please verify your email by clicking the link below:

{verification_url}

This link expires in 24 hours.

If you didn't create this account, ignore this email.

— Xenohuru Team
        """

        send_mail(
            subject='Welcome to Xenohuru - Verify Your Email',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"Verification email sent to {user.email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        return False


def send_welcome_email(user):
    try:
        message = f"""Hello {user.username},

Your email has been verified! You now have full access to the Xenohuru API.

API docs: https://xenohuru.cleven.is-a.dev/api/docs/

Happy exploring!
— Xenohuru Team
        """

        send_mail(
            subject='Xenohuru - Email Verified',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        logger.info(f"Welcome email sent to {user.email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False
