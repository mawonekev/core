from datetime import timedelta

from django.db.models import Avg, Count
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from app.attractions.models import Attraction
from app.blog.models import Article
from app.regions.models import Region

from .models import APIUsage, Statistics
from .serializers import APIUsageSerializer, StatisticsSerializer


def _site_url():
    from django.conf import settings
    return getattr(settings, 'FRONTEND_URL', 'https://xenohuru.com').rstrip('/')


def robots_txt(request):
    base = _site_url()
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /api/",
        "",
        f"Sitemap: {base}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    base = _site_url()

    STATIC = [
        ('',              1.0, 'daily'),
        ('attractions',   0.95, 'daily'),
        ('regions',       0.90, 'weekly'),
        ('blog',          0.85, 'daily'),
        ('weather',       0.80, 'hourly'),
        ('search',        0.75, 'weekly'),
        ('itineraries',   0.70, 'monthly'),
        ('faq',           0.70, 'monthly'),
        ('about',         0.60, 'monthly'),
        ('contact',       0.55, 'yearly'),
        ('sponsor',       0.55, 'monthly'),
    ]

    def url(loc, lastmod=None, changefreq='monthly', priority=0.5):
        parts = [f'<loc>{loc}</loc>']
        if lastmod:
            parts.append(f'<lastmod>{lastmod}</lastmod>')
        parts.append(f'<changefreq>{changefreq}</changefreq>')
        parts.append(f'<priority>{priority}</priority>')
        return '<url>' + ''.join(parts) + '</url>'

    urls = []
    for path, pri, freq in STATIC:
        loc = base if not path else f'{base}/{path}'
        urls.append(url(loc, changefreq=freq, priority=pri))

    for a in Attraction.objects.filter(is_active=True, is_approved=True, deleted_at__isnull=True).values('slug', 'updated_at', 'is_featured'):
        urls.append(url(
            f'{base}/attractions/{a["slug"]}',
            lastmod=a['updated_at'].strftime('%Y-%m-%d'),
            changefreq='weekly',
            priority=0.9 if a['is_featured'] else 0.8,
        ))

    for r in Region.objects.filter(is_approved=True, deleted_at__isnull=True).values('slug', 'updated_at'):
        urls.append(url(
            f'{base}/regions/{r["slug"]}',
            lastmod=r['updated_at'].strftime('%Y-%m-%d'),
            changefreq='monthly',
            priority=0.75,
        ))

    for art in Article.objects.filter(status='published', is_approved=True, deleted_at__isnull=True).values('slug', 'updated_at'):
        urls.append(url(
            f'{base}/blog/{art["slug"]}',
            lastmod=art['updated_at'].strftime('%Y-%m-%d'),
            changefreq='monthly',
            priority=0.70,
        ))

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(urls)
        + '\n</urlset>'
    )
    return HttpResponse(xml, content_type='application/xml')


def health_check(request):
    from django.conf import settings
    db_path = str(settings.DATABASES['default']['NAME'])
    try:
        region_count = Region.objects.filter(deleted_at__isnull=True).count()
        attraction_count = Attraction.objects.filter(deleted_at__isnull=True).count()
        db_status = 'ok'
    except Exception as e:
        region_count = -1
        attraction_count = -1
        db_status = str(e)

    return JsonResponse({
        'status': 'ok',
        'timestamp': timezone.now().isoformat(),
        'service': 'Xenohuru API',
        'db_path': db_path,
        'db_status': db_status,
        'regions': region_count,
        'attractions': attraction_count,
    })


class StatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for system statistics.
    Admin only.
    """
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        """Get current system statistics"""
        stats = Statistics.get_instance()
        serializer = self.get_serializer(stats)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Get statistics by ID (always returns singleton)"""
        stats = Statistics.get_instance()
        serializer = self.get_serializer(stats)
        return Response(serializer.data)


class APIUsageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tracking API usage.
    Admin only.

    Provides endpoints for:
    - List all API calls
    - Filter by endpoint, method, status code, user, date range
    - Analytics: top endpoints, top users, response time stats
    """
    queryset = APIUsage.objects.all()
    serializer_class = APIUsageSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['endpoint', 'method', 'status_code', 'user', 'timestamp']
    ordering_fields = ['timestamp', 'response_time_ms', 'status_code']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Get analytics data:
        - Total API calls (all time, today, last 30 days)
        - Top endpoints
        - Top users
        - Average response time
        - Status code distribution
        """
        now = timezone.now()
        today = now.date()
        last_30_days = now - timedelta(days=30)

        # Query aggregates
        total_calls = APIUsage.objects.count()
        calls_today = APIUsage.objects.filter(timestamp__date=today).count()
        calls_last_30_days = APIUsage.objects.filter(timestamp__gte=last_30_days).count()

        top_endpoints = (
            APIUsage.objects
            .values('endpoint')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        top_users = (
            APIUsage.objects
            .filter(user__isnull=False)
            .values('user__username', 'user__email')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        status_distribution = (
            APIUsage.objects
            .values('status_code')
            .annotate(count=Count('id'))
            .order_by('-status_code')
        )

        avg_response_time = APIUsage.objects.aggregate(
            avg=Avg('response_time_ms')
        )['avg'] or 0

        # Method distribution
        method_distribution = (
            APIUsage.objects
            .values('method')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response({
            'total_calls': total_calls,
            'calls_today': calls_today,
            'calls_last_30_days': calls_last_30_days,
            'avg_response_time_ms': round(avg_response_time, 2),
            'top_endpoints': list(top_endpoints),
            'top_users': list(top_users),
            'status_distribution': list(status_distribution),
            'method_distribution': list(method_distribution),
        })

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get API calls grouped by status code"""
        status_code = request.query_params.get('status_code')
        if not status_code:
            return Response(
                {'error': 'status_code parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        calls = APIUsage.objects.filter(
            status_code=status_code
        ).order_by('-timestamp')
        serializer = self.get_serializer(calls, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get API calls for a specific user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        calls = APIUsage.objects.filter(
            user__id=user_id
        ).order_by('-timestamp')
        serializer = self.get_serializer(calls, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_endpoint(self, request):
        """Get API calls for a specific endpoint"""
        endpoint = request.query_params.get('endpoint')
        if not endpoint:
            return Response(
                {'error': 'endpoint parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        calls = APIUsage.objects.filter(
            endpoint__icontains=endpoint
        ).order_by('-timestamp')
        serializer = self.get_serializer(calls, many=True)
        return Response(serializer.data)
