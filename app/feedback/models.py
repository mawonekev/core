from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class UserFeedback(models.Model):
    FEEDBACK_TYPES = [
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('correction', 'Correction'),
        ('compliment', 'Compliment'),
        ('report_error', 'Report Error'),
        ('partnership_inquiry', 'Partnership Inquiry'),
        ('operator_inquiry', 'Operator Inquiry'),
        ('media_submission', 'Media Submission'),
        ('general', 'General'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_TYPES, default='general')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    attachment = CloudinaryField('attachment', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    response = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'User Feedback'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_feedback_type_display()}: {self.subject}"


class Review(models.Model):
    VISIT_TYPES = [
        ('solo', 'Solo'),
        ('couple', 'Couple'),
        ('family', 'Family'),
        ('group', 'Group'),
        ('business', 'Business'),
    ]
    VISIT_SEASONS = [
        ('dry', 'Dry Season'),
        ('long_rains', 'Long Rains'),
        ('short_rains', 'Short Rains'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    attraction = models.ForeignKey('attractions.Attraction', on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=255, blank=True)
    reviewer_email = models.EmailField(blank=True)
    reviewer_country = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating = models.IntegerField()
    rating_scenery = models.IntegerField(null=True, blank=True)
    rating_accessibility = models.IntegerField(null=True, blank=True)
    rating_value_for_money = models.IntegerField(null=True, blank=True)
    rating_safety = models.IntegerField(null=True, blank=True)
    rating_facilities = models.IntegerField(null=True, blank=True)
    visited_at = models.DateField(null=True, blank=True)
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPES, blank=True)
    visit_season = models.CharField(max_length=50, choices=VISIT_SEASONS, blank=True)
    photos = models.ManyToManyField('media.Media', blank=True, related_name='reviews')
    is_approved = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        reviewer = self.user.username if self.user else self.reviewer_name or 'Anonymous'
        return f"Review by {reviewer} for {self.attraction.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.user and not (self.reviewer_name and self.reviewer_email):
            raise ValidationError('Either user or reviewer name/email must be provided')
        if self.user:
            existing = Review.objects.filter(user=self.user, attraction=self.attraction)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError(f'You have already reviewed {self.attraction.name}')
