from django.db import models

from app.core.models import BaseModel


class Announcement(BaseModel):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    TYPE_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('promo', 'Promotion'),
        ('maintenance', 'Maintenance'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True, help_text='When to show this announcement')
    ends_at = models.DateTimeField(null=True, blank=True, help_text='When to hide this announcement')
    target_url = models.URLField(blank=True, help_text='Optional CTA link')
    target_label = models.CharField(max_length=100, blank=True, help_text='CTA button label')

    class Meta:
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'ends_at']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return self.title
