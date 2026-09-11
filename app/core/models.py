from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class SoftDeleteManager(models.Manager):
    """Manager that filters out soft-deleted records (deleted_at is NULL)"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class AllObjectsManager(models.Manager):
    """Manager that includes all records, including soft-deleted ones"""
    def get_queryset(self):
        return super().get_queryset()


class BaseModel(models.Model):
    """Base model with soft delete and approval. deleted_at=null means active."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_approved = models.BooleanField(default=False, db_index=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    def delete(self, hard=False, *args, **kwargs):
        if hard:
            super().delete(*args, **kwargs)
        else:
            self.deleted_at = timezone.now()
            self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def approve(self):
        self.is_approved = True
        self.save()

    def reject(self):
        self.is_approved = False
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Statistics(models.Model):
    """Singleton — tracks system-wide counts, updated by signals."""
    total_attractions = models.IntegerField(default=0)
    total_regions = models.IntegerField(default=0)
    total_operators = models.IntegerField(default=0)
    total_blog_articles = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    total_api_calls = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Statistics'

    def __str__(self):
        return 'System Statistics'

    @classmethod
    def get_instance(cls):
        """Get or create the singleton statistics record"""
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance

    @classmethod
    def update(cls):
        """Update all statistics from current database state"""
        from app.accounts.models import User
        from app.attractions.models import Attraction
        from app.blog.models import Article
        from app.operators.models import TourOperator
        from app.regions.models import Region

        instance = cls.get_instance()
        instance.total_attractions = Attraction.objects.count()
        instance.total_regions = Region.objects.count()
        instance.total_operators = TourOperator.objects.count()
        instance.total_blog_articles = Article.objects.count()
        instance.total_users = User.objects.count()
        instance.save()

        return instance


class UserActivityLog(models.Model):
    ACTION_CHOICES = [
        ('view_attraction', 'Viewed Attraction'),
        ('view_region',     'Viewed Region'),
        ('view_article',    'Viewed Article'),
        ('search',          'Searched'),
        ('submit_review',   'Submitted Review'),
        ('view_itinerary',  'Viewed Itinerary'),
    ]

    user        = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='activity_logs')
    action      = models.CharField(max_length=50, choices=ACTION_CHOICES, db_index=True)
    object_type = models.CharField(max_length=50, blank=True)
    object_id   = models.CharField(max_length=200, blank=True)
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    metadata    = models.JSONField(default=dict, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action', 'created_at']),
            models.Index(fields=['object_type', 'object_id']),
        ]

    def __str__(self):
        who = self.user.username if self.user else f'anon:{self.ip_address}'
        return f'{who} — {self.action} — {self.object_id}'


class APIUsage(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        null=True,
        blank=True,  # null = anonymous request
        on_delete=models.SET_NULL,
        related_name='api_usage'
    )
    endpoint = models.CharField(max_length=500, db_index=True)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    response_time_ms = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['endpoint', 'timestamp']),
            models.Index(fields=['status_code', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code}"
