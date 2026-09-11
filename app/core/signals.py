from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Statistics


@receiver(post_save, sender='attractions.Attraction')
@receiver(post_delete, sender='attractions.Attraction')
def update_stats_on_attraction_change(sender, **kwargs):
    """Update statistics when an Attraction is created/deleted"""
    Statistics.update()


@receiver(post_save, sender='regions.Region')
@receiver(post_delete, sender='regions.Region')
def update_stats_on_region_change(sender, **kwargs):
    """Update statistics when a Region is created/deleted"""
    Statistics.update()


@receiver(post_save, sender='operators.TourOperator')
@receiver(post_delete, sender='operators.TourOperator')
def update_stats_on_operator_change(sender, **kwargs):
    """Update statistics when a TourOperator is created/deleted"""
    Statistics.update()


@receiver(post_save, sender='blog.Article')
@receiver(post_delete, sender='blog.Article')
def update_stats_on_article_change(sender, **kwargs):
    """Update statistics when an Article is created/deleted"""
    Statistics.update()


@receiver(post_save, sender='accounts.User')
@receiver(post_delete, sender='accounts.User')
def update_stats_on_user_change(sender, **kwargs):
    """Update statistics when a User is created/deleted"""
    Statistics.update()
