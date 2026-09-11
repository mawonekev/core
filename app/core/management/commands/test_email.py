"""
Management command to test email configuration
Usage: python manage.py test_email your-email@example.com
"""
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            'recipient',
            type=str,
            help='Email address to send test email to'
        )

    def handle(self, *args, **options):
        recipient = options['recipient']

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write("  Testing Email Configuration")
        self.stdout.write(f"{'='*60}\n")

        # Check configuration
        self.stdout.write("Configuration:")
        self.stdout.write(f"  Backend:     {settings.EMAIL_BACKEND}")
        self.stdout.write(f"  Host:        {getattr(settings, 'EMAIL_HOST', 'Not set')}")
        self.stdout.write(f"  Port:        {getattr(settings, 'EMAIL_PORT', 'Not set')}")
        self.stdout.write(f"  TLS:         {getattr(settings, 'EMAIL_USE_TLS', False)}")
        self.stdout.write(f"  From:        {settings.DEFAULT_FROM_EMAIL}")

        email_user = getattr(settings, 'EMAIL_HOST_USER', None)
        if email_user:
            self.stdout.write(f"  Username:    {email_user}")
        else:
            self.stdout.write(self.style.WARNING("  ⚠ EMAIL_HOST_USER not configured!"))

        email_pass = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
        if email_pass:
            self.stdout.write(f"  Password:    {'*' * len(email_pass)} (configured)")
        else:
            self.stdout.write(self.style.WARNING("  ⚠ EMAIL_HOST_PASSWORD not configured!"))

        self.stdout.write(f"\nSending test email to: {recipient}")

        # Send test email
        try:
            result = send_mail(
                subject='[Xenohuru API] Test Email',
                message=(
                    'Congratulations! Your email configuration is working.\n\n'
                    'This is a test email from the Xenohuru API.\n\n'
                    'Email features enabled:\n'
                    '  ✓ Feedback notifications\n'
                    '  ✓ Review moderation alerts\n'
                    '  ✓ Admin notifications\n\n'
                    'If you received this email, your SMTP settings are correctly configured.\n\n'
                    '---\n'
                    'Xenohuru API - Explore the Magic of Tanzania 🇹🇿'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )

            if result == 1:
                self.stdout.write(self.style.SUCCESS("\n✓ Success! Test email sent successfully."))
                self.stdout.write(self.style.SUCCESS(f"  Check {recipient} inbox (and spam folder).\n"))
            else:
                self.stdout.write(self.style.ERROR(f"\n✗ Failed to send email (returned {result})\n"))

        except Exception as e:
            self.stdout.write(self.style.ERROR("\n✗ Error sending email:"))
            self.stdout.write(self.style.ERROR(f"  {type(e).__name__}: {str(e)}\n"))

            # Troubleshooting hints
            self.stdout.write(self.style.WARNING("Troubleshooting:"))
            if 'Authentication' in str(e):
                self.stdout.write(self.style.WARNING("  → Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD"))
                self.stdout.write(self.style.WARNING("  → For Gmail, enable 2FA and use App Password"))
            elif 'Connection' in str(e) or 'refused' in str(e):
                self.stdout.write(self.style.WARNING("  → Check EMAIL_HOST and EMAIL_PORT"))
                self.stdout.write(self.style.WARNING("  → Verify firewall allows outbound SMTP"))
            elif 'timed out' in str(e):
                self.stdout.write(self.style.WARNING("  → Network timeout - check internet connection"))

            self.stdout.write("\nSee EMAIL_SETUP.md for detailed configuration guide.\n")
            return

        self.stdout.write(f"{'='*60}\n")
