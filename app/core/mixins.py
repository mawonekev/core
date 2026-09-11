from cloudinary.models import CloudinaryField
from django.db import models


class SEOMixin(models.Model):
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.CharField(max_length=500, blank=True)
    og_image = models.ForeignKey(
        'media.Media',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        help_text='Social share image'
    )
    canonical_url = models.URLField(blank=True)
    schema_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('TouristAttraction', 'Tourist Attraction'),
            ('Article', 'Article'),
            ('Person', 'Person'),
            ('Organization', 'Organization'),
        ]
    )
    schema_json = models.JSONField(null=True, blank=True, help_text='Full JSON-LD structured data')
    no_index = models.BooleanField(default=False, help_text='Hide from search engines')
    sitemap_priority = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    sitemap_changefreq = models.CharField(
        max_length=20,
        choices=[
            ('always', 'Always'),
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('never', 'Never'),
        ],
        default='monthly'
    )

    class Meta:
        abstract = True


class ContactMixin(models.Model):
    phone = models.CharField(max_length=30, blank=True)
    phone_secondary = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)

    class Meta:
        abstract = True


class LocationMixin(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.CASCADE,
        related_name='%(class)s_locations',
    )

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    featured_image = CloudinaryField('image', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class PublishMixin(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class PriceMixin(models.Model):
    CURRENCY_CHOICES = [
        ('TZS', 'Tanzanian Shilling'),
        ('USD', 'US Dollar'),
    ]

    price_from = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Minimum price'
    )
    price_to = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Maximum price (optional)'
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD'
    )
    is_free = models.BooleanField(
        default=False,
        help_text='Mark as free if no entrance fee'
    )

    class Meta:
        abstract = True
