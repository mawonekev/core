from django.conf import settings


def site_url(request):
    base = getattr(settings, 'FRONTEND_URL', 'https://xenohuru.com').rstrip('/')
    canonical = base + request.path.rstrip('/')
    return {
        'SITE_URL': base,
        'CANONICAL_URL': canonical,
    }
