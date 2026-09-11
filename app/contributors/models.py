from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

from app.core.mixins import SEOMixin

User = get_user_model()

class CreatorProfile(SEOMixin, models.Model):
    EXPERTISE_CHOICES = [
        ('wildlife', 'Wildlife'),
        ('photography', 'Photography'),
        ('hiking', 'Hiking'),
        ('culture', 'Culture'),
        ('marine', 'Marine'),
        ('geology', 'Geology'),
    ]

    # CORE
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator_profile')
    username = models.CharField(max_length=150, unique=True, help_text='Public @handle')
    display_name = models.CharField(max_length=200, help_text='Full public name')
    avatar = CloudinaryField('avatar', blank=True, null=True)
    avatar_alt = models.CharField(max_length=200, blank=True, help_text='Alt text for avatar')
    bio = models.TextField(max_length=280, blank=True, help_text='Short bio (280 chars)')
    job_title = models.CharField(max_length=150, blank=True, help_text='e.g. "Wildlife Photographer"')
    organisation = models.CharField(max_length=200, blank=True, help_text='e.g. "Serengeti Research Institute"')
    expertise = models.CharField(max_length=50, choices=EXPERTISE_CHOICES, blank=True)

    # SOCIAL / CONTACT
    website = models.URLField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    twitter_handle = models.CharField(max_length=100, blank=True)
    instagram_handle = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    email_public = models.EmailField(blank=True, help_text='Optional public email')

    # LOCATION
    location_city = models.CharField(max_length=100, blank=True, help_text='e.g. "Arusha"')
    location_country = models.CharField(max_length=100, default='Tanzania')

    # CONTRIBUTION STATS (Cooled down/auto-calculated in practice)
    attractions_created = models.IntegerField(default=0)
    attractions_edited = models.IntegerField(default=0)
    media_uploaded = models.IntegerField(default=0)
    articles_written = models.IntegerField(default=0)
    species_added = models.IntegerField(default=0)

    # PROFILE PAGE
    is_public = models.BooleanField(default=True, help_text='Public profile page visible')
    is_verified_creator = models.BooleanField(default=False, help_text='Xenohuru verified badge')

    # TIMESTAMPS
    joined_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.username
