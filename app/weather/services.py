from decimal import Decimal

import requests
from django.conf import settings
from django.core.cache import cache

from .models import WeatherCache


class WeatherService:
    BASE_URL = settings.WEATHER_API_BASE_URL
    CACHE_TIMEOUT = settings.WEATHER_CACHE_TIMEOUT

    @classmethod
    def get_weather_code_description(cls, code):
        weather_codes = {
            0: 'Clear sky',
            1: 'Mainly clear',
            2: 'Partly cloudy',
            3: 'Overcast',
            45: 'Foggy',
            48: 'Depositing rime fog',
            51: 'Light drizzle',
            53: 'Moderate drizzle',
            55: 'Dense drizzle',
            61: 'Slight rain',
            63: 'Moderate rain',
            65: 'Heavy rain',
            71: 'Slight snow',
            73: 'Moderate snow',
            75: 'Heavy snow',
            77: 'Snow grains',
            80: 'Slight rain showers',
            81: 'Moderate rain showers',
            82: 'Violent rain showers',
            85: 'Slight snow showers',
            86: 'Heavy snow showers',
            95: 'Thunderstorm',
            96: 'Thunderstorm with slight hail',
            99: 'Thunderstorm with heavy hail',
        }
        return weather_codes.get(code, 'Unknown')

    @classmethod
    def fetch_current_weather(cls, latitude, longitude):
        cache_key = f'weather_current_{latitude}_{longitude}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        params = {
            'latitude': float(latitude),
            'longitude': float(longitude),
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m,surface_pressure,visibility',
            'hourly': 'precipitation_probability,uv_index',
            'forecast_days': 1,
            'timezone': 'Africa/Dar_es_Salaam',
        }

        try:
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            current = data.get('current', {})
            weather_data = {
                'temperature': current.get('temperature_2m'),
                'apparent_temperature': current.get('apparent_temperature'),
                'humidity': current.get('relative_humidity_2m'),
                'precipitation': current.get('precipitation'),
                'rain': current.get('rain'),
                'weather_code': current.get('weather_code'),
                'weather_description': cls.get_weather_code_description(current.get('weather_code', 0)),
                'cloud_cover': current.get('cloud_cover'),
                'wind_speed': current.get('wind_speed_10m'),
                'wind_direction': current.get('wind_direction_10m'),
                'surface_pressure': current.get('surface_pressure'),
                'visibility': current.get('visibility'),
                'precipitation_probability': data.get('hourly', {}).get('precipitation_probability', [None])[0],
                'uv_index': data.get('hourly', {}).get('uv_index', [None])[0],
                'timestamp': current.get('time'),
            }

            # Store in cache
            cache.set(cache_key, weather_data, cls.CACHE_TIMEOUT)

            # Store in database for persistence (fallback if API fails later)
            cls._save_to_database(latitude, longitude, weather_data)

            return weather_data

        except requests.RequestException as e:
            # If API fails, try to get from database
            db_weather = cls._get_from_database(latitude, longitude)
            if db_weather:
                db_weather['source'] = 'database_fallback'
                db_weather['warning'] = 'Weather API unavailable, showing cached data'
                return db_weather
            return {'error': f'Weather API error: {str(e)}'}

    @classmethod
    def _save_to_database(cls, latitude, longitude, weather_data):
        """Save weather data to database for persistence"""
        try:
            from app.attractions.models import Attraction

            # Find attraction with these coordinates
            attraction = Attraction.objects.filter(
                latitude=Decimal(str(latitude)),
                longitude=Decimal(str(longitude))
            ).first()

            if attraction:
                # Update or create weather cache
                WeatherCache.objects.update_or_create(
                    attraction=attraction,
                    defaults={
                        'temperature': weather_data.get('temperature'),
                        'apparent_temperature': weather_data.get('apparent_temperature'),
                        'precipitation': weather_data.get('precipitation'),
                        'rain': weather_data.get('rain'),
                        'weather_code': weather_data.get('weather_code'),
                        'cloud_cover': weather_data.get('cloud_cover'),
                        'wind_speed': weather_data.get('wind_speed'),
                        'humidity': weather_data.get('humidity'),
                    }
                )
        except Exception as e:
            # Don't fail if database save fails
            import logging
            logger = logging.getLogger('app.weather')
            logger.error(f"Failed to save weather to database: {e}")

    @classmethod
    def _get_from_database(cls, latitude, longitude):
        """Get weather data from database as fallback"""
        try:
            from datetime import timedelta

            from django.utils import timezone

            from app.attractions.models import Attraction

            # Find attraction with these coordinates
            attraction = Attraction.objects.filter(
                latitude=Decimal(str(latitude)),
                longitude=Decimal(str(longitude))
            ).first()

            if attraction:
                try:
                    weather_cache = WeatherCache.objects.get(attraction=attraction)

                    # Check if data is not too old (less than 7 days)
                    if weather_cache.last_updated > timezone.now() - timedelta(days=7):
                        return {
                            'temperature': float(weather_cache.temperature) if weather_cache.temperature else None,
                            'apparent_temperature': float(weather_cache.apparent_temperature) if weather_cache.apparent_temperature else None,
                            'humidity': weather_cache.humidity,
                            'precipitation': float(weather_cache.precipitation) if weather_cache.precipitation else None,
                            'rain': float(weather_cache.rain) if weather_cache.rain else None,
                            'weather_code': weather_cache.weather_code,
                            'weather_description': cls.get_weather_code_description(weather_cache.weather_code) if weather_cache.weather_code else 'Unknown',
                            'cloud_cover': weather_cache.cloud_cover,
                            'wind_speed': float(weather_cache.wind_speed) if weather_cache.wind_speed else None,
                            'timestamp': weather_cache.last_updated.isoformat(),
                            'data_age_days': (timezone.now() - weather_cache.last_updated).days,
                        }
                except WeatherCache.DoesNotExist:
                    pass

        except Exception as e:
            import logging
            logger = logging.getLogger('app.weather')
            logger.error(f"Failed to get weather from database: {e}")

        return None

    @classmethod
    def fetch_forecast(cls, latitude, longitude, days=7):
        cache_key = f'weather_forecast_{latitude}_{longitude}_{days}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        params = {
            'latitude': float(latitude),
            'longitude': float(longitude),
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,weather_code,precipitation_probability_max,wind_speed_10m_max,uv_index_max,relative_humidity_2m_max,relative_humidity_2m_min',
            'timezone': 'Africa/Dar_es_Salaam',
            'forecast_days': days,
        }

        try:
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            daily = data.get('daily', {})
            forecast_data = {
                'dates': daily.get('time', []),
                'temperature_max': daily.get('temperature_2m_max', []),
                'temperature_min': daily.get('temperature_2m_min', []),
                'precipitation': daily.get('precipitation_sum', []),
                'rain': daily.get('rain_sum', []),
                'weather_codes': daily.get('weather_code', []),
                'weather_descriptions': [cls.get_weather_code_description(c) for c in daily.get('weather_code', [])],
                'precipitation_probability': daily.get('precipitation_probability_max', []),
                'wind_speed_max': daily.get('wind_speed_10m_max', []),
                'uv_index_max': daily.get('uv_index_max', []),
                'humidity_max': daily.get('relative_humidity_2m_max', []),
                'humidity_min': daily.get('relative_humidity_2m_min', []),
            }

            cache.set(cache_key, forecast_data, cls.CACHE_TIMEOUT)
            return forecast_data

        except requests.RequestException as e:
            return {'error': f'Weather API error: {str(e)}'}

    @classmethod
    def fetch_historical_weather(cls, latitude, longitude, days=7):
        """Fetch historical weather from Open-Meteo Archive API. Max 90 days."""
        from datetime import date, timedelta
        days = min(int(days), 90)
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=days - 1)

        cache_key = f'weather_historical_{latitude}_{longitude}_{days}'
        cached = cache.get(cache_key)
        if cached:
            return cached

        params = {
            'latitude': float(latitude),
            'longitude': float(longitude),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'daily': 'temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,rain_sum,relative_humidity_2m_max,relative_humidity_2m_min,wind_speed_10m_max,weather_code',
            'timezone': 'Africa/Dar_es_Salaam',
        }

        try:
            response = requests.get(
                'https://archive-api.open-meteo.com/v1/archive',
                params=params, timeout=15
            )
            response.raise_for_status()
            data = response.json()
            daily = data.get('daily', {})
            weather_codes = daily.get('weather_code', [])

            result = {
                'period': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat(),
                    'days': days,
                },
                'dates': daily.get('time', []),
                'temperature_max': daily.get('temperature_2m_max', []),
                'temperature_min': daily.get('temperature_2m_min', []),
                'temperature_mean': daily.get('temperature_2m_mean', []),
                'precipitation_sum': daily.get('precipitation_sum', []),
                'rain_sum': daily.get('rain_sum', []),
                'humidity_max': daily.get('relative_humidity_2m_max', []),
                'humidity_min': daily.get('relative_humidity_2m_min', []),
                'wind_speed_max': daily.get('wind_speed_10m_max', []),
                'weather_codes': weather_codes,
                'weather_descriptions': [cls.get_weather_code_description(c) for c in weather_codes],
            }
            cache.set(cache_key, result, 3600 * 6)  # 6-hour cache
            return result

        except requests.RequestException as e:
            return {'error': f'Historical weather API error: {str(e)}'}

    @classmethod
    def update_attraction_weather_cache(cls, attraction):
        weather_data = cls.fetch_current_weather(attraction.latitude, attraction.longitude)

        if 'error' not in weather_data:
            cache_obj, created = WeatherCache.objects.get_or_create(attraction=attraction)
            cache_obj.temperature = weather_data.get('temperature')
            cache_obj.apparent_temperature = weather_data.get('apparent_temperature')
            cache_obj.precipitation = weather_data.get('precipitation')
            cache_obj.rain = weather_data.get('rain')
            cache_obj.weather_code = weather_data.get('weather_code')
            cache_obj.cloud_cover = weather_data.get('cloud_cover')
            cache_obj.wind_speed = weather_data.get('wind_speed')
            cache_obj.humidity = weather_data.get('humidity')
            cache_obj.save()

            return cache_obj

        return None
