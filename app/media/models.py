from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Media(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('360_photo', '360 Photo'),
        ('drone', 'Drone Footage'),
        ('audio', 'Audio'),
    ]

    LICENSES = [
        ('CC0', 'CC0'),
        ('CC-BY', 'CC-BY'),
        ('CC-BY-SA', 'CC-BY-SA'),
        ('proprietary', 'Proprietary'),
    ]

    file = CloudinaryField('file', blank=True, null=True)
    url = models.URLField(blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default='image')
    title = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    credit = models.CharField(max_length=200, blank=True)
    credit_url = models.URLField(blank=True)
    license = models.CharField(max_length=20, choices=LICENSES, default='proprietary')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_cover = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    file_size_kb = models.IntegerField(null=True, blank=True)
    taken_at = models.DateField(null=True, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_media')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Media'
        ordering = ['sort_order', '-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return self.title or f"{self.get_media_type_display()} {self.id}"
