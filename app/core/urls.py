from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIUsageViewSet, StatisticsViewSet

router = DefaultRouter()
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'api-usage', APIUsageViewSet, basename='api-usage')

urlpatterns = [
    path('', include(router.urls)),
]
