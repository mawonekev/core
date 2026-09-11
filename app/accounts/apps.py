import os
import threading
import time

from django.apps import AppConfig


class accountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.accounts'

    def ready(self):
        # Import signals
        import app.accounts.signals  # noqa

        if not os.environ.get('RENDER'):
            return

        from django.conf import settings
        base_url = getattr(settings, 'RENDER_EXTERNAL_URL', '').rstrip('/')
        if not base_url:
            return

        # ── Keep-alive: ping every 2 min to prevent free-tier sleep ──
        def keep_alive():
            time.sleep(60)  # Wait for server to fully start
            while True:
                try:
                    import requests
                    requests.get(f'{base_url}/api/health/', timeout=10)
                except Exception:
                    pass
                time.sleep(2 * 60)  # Every 2 min

        # ── Cache warmer: refresh weather + featured attractions ──
        def cache_warmer():
            time.sleep(120)  # Wait for DB/app to be fully ready
            while True:
                try:
                    _warm_weather_cache()
                    _warm_attractions_cache(base_url)
                except Exception:
                    pass
                time.sleep(10 * 60)  # Refresh every 10 min

        threading.Thread(target=keep_alive, daemon=True).start()
        threading.Thread(target=cache_warmer, daemon=True).start()


def _warm_weather_cache():
    """Pre-fetch weather for all active attractions that have coordinates."""
    try:
        from app.attractions.models import Attraction
        from app.weather.services import WeatherService
        attractions = Attraction.objects.filter(
            is_active=True, latitude__isnull=False, longitude__isnull=False
        ).values('latitude', 'longitude')[:50]  # top 50 to stay within rate limits
        for a in attractions:
            try:
                WeatherService.fetch_current_weather(a['latitude'], a['longitude'])
            except Exception:
                pass
    except Exception:
        pass


def _warm_attractions_cache(base_url):
    """Hit the public list + featured endpoints so they're cached for real users."""
    try:
        import requests
        endpoints = [
            '/api/v1/attractions/',
            '/api/v1/attractions/?is_featured=true',
            '/api/v1/regions/',
        ]
        for path in endpoints:
            try:
                requests.get(f'{base_url}{path}', timeout=15)
            except Exception:
                pass
    except Exception:
        pass
