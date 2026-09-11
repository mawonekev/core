import time

from django.utils.deprecation import MiddlewareMixin

from .models import APIUsage, Statistics, UserActivityLog

_ROUTE_MAP = {
    'web:attraction-detail': ('view_attraction', 'attraction'),
    'web:region-detail':     ('view_region',     'region'),
    'web:blog-detail':       ('view_article',    'article'),
    'web:itinerary-detail':  ('view_itinerary',  'itinerary'),
}


def _get_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')


class ActivityLogMiddleware(MiddlewareMixin):
    """Logs meaningful web page views and searches to UserActivityLog."""

    def process_response(self, request, response):
        if response.status_code != 200 or request.method != 'GET':
            return response
        try:
            match = request.resolver_match
            if not match:
                return response
            view_name = match.view_name
            if view_name in _ROUTE_MAP:
                action, obj_type = _ROUTE_MAP[view_name]
                slug = match.kwargs.get('slug', '')
                UserActivityLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    action=action,
                    object_type=obj_type,
                    object_id=slug,
                    ip_address=_get_ip(request),
                )
            elif view_name == 'web:search' and request.GET.get('q'):
                UserActivityLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    action='search',
                    object_type='query',
                    object_id=request.GET['q'][:200],
                    ip_address=_get_ip(request),
                )
        except Exception:
            pass
        return response


class APIUsageMiddleware(MiddlewareMixin):
    """
    Middleware that tracks all API requests to /api/ endpoints.
    Records endpoint, method, status code, IP, user agent, and response time.
    """

    def process_request(self, request):
        # Store start time for response time calculation
        request._start_time = time.time()
        return None

    def process_response(self, request, response):
        # Only track API endpoints
        if not request.path.startswith('/api/'):
            return response

        # Skip tracking for schema/docs endpoints
        if request.path.startswith('/api/schema/') or request.path.startswith('/api/docs/'):
            return response

        # Calculate response time
        start_time = getattr(request, '_start_time', time.time())
        response_time_ms = int((time.time() - start_time) * 1000)

        try:
            # Get user if authenticated
            user = request.user if request.user.is_authenticated else None

            # Get IP address (handle proxies)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            # Create APIUsage record
            APIUsage.objects.create(
                user=user,
                endpoint=request.path,
                method=request.method,
                status_code=response.status_code,
                ip_address=ip_address,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                response_time_ms=response_time_ms,
            )

            # Update total API calls in statistics
            stats = Statistics.get_instance()
            stats.total_api_calls = APIUsage.objects.count()
            stats.save(update_fields=['total_api_calls', 'updated_at'])

        except Exception as e:
            # Silently fail to avoid breaking request/response cycle
            import logging
            logger = logging.getLogger(__name__)
            logger.exception(f"Error tracking API usage: {e}")

        return response
