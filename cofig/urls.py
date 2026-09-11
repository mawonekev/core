from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from app.core.views import health_check, robots_txt, sitemap_xml

urlpatterns = [
    path('robots.txt', robots_txt, name='robots-txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
    path('api/health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('', include('app.web.urls')),

    # API v1 endpoints
    path('api/v1/auth/', include('app.accounts.urls')),
    path('api/v1/core/', include('app.core.urls')),
    path('api/v1/regions/', include('app.regions.urls')),
    path('api/v1/attractions/', include('app.attractions.urls')),
    path('api/v1/weather/', include('app.weather.urls')),
    path('api/v1/operators/', include('app.operators.urls')),
    path('api/v1/partners/', include('app.partners.urls')),
    path('api/v1/blog/', include('app.blog.urls')),
    path('api/v1/media/', include('app.media.urls')),
    path('api/v1/contributors/', include('app.contributors.urls')),
    path('api/v1/feedback/', include('app.feedback.urls')),
    path('api/v1/itinerary/', include('app.itinerary.urls')),
    # Announcements — auth-required, hidden from public docs
    path('api/v1/announcements/', include('app.announcements.urls')),

    # API schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
