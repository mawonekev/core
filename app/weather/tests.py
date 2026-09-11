from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from app.attractions.models import Attraction
from app.regions.models import Region

from .models import SeasonalWeatherPattern

User = get_user_model()


def make_attraction(region, user):
    return Attraction.objects.create(
        name='Kilimanjaro', slug='kilimanjaro', region=region,
        category='mountain', description='Africa\'s highest mountain.',
        short_description='Highest peak.', latitude='-3.0674', longitude='37.3556',
        difficulty_level='extreme', access_info='Via Moshi town.',
        best_time_to_visit='Jan, Feb, Jun-Oct', seasonal_availability='Year-round',
        estimated_duration='5-9 days', created_by=user, is_active=True,
    )


class WeatherAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='wxuser', email='wx@example.com', password='Pass1234!')
        self.region = Region.objects.create(
            name='Kilimanjaro Region', slug='kilimanjaro-region', description='Mountain region.',
            latitude='-3.0674', longitude='37.3556',
        )
        self.attraction = make_attraction(self.region, self.user)

    def test_weather_list(self):
        response = self.client.get('/api/v1/weather/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_weather_detail_not_found(self):
        response = self.client.get('/api/v1/weather/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_current_weather_missing_params(self):
        response = self.client.get('/api/v1/weather/current/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_current_weather_with_coords(self):
        mock_data = {
            'temperature': 20.5, 'apparent_temperature': 19.0, 'precipitation': 0.0,
            'rain': 0.0, 'weather_code': 0, 'cloud_cover': 10,
            'wind_speed': 5.0, 'humidity': 60,
        }
        with patch('app.weather.views.WeatherService.fetch_current_weather', return_value=mock_data):
            response = self.client.get('/api/v1/weather/current/?lat=-3.0674&lon=37.3556')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_weather_attraction_not_found(self):
        response = self.client.get('/api/v1/weather/current/?attraction=nonexistent')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_forecast_missing_params(self):
        response = self.client.get('/api/v1/weather/forecast/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seasonal_missing_param(self):
        response = self.client.get('/api/v1/weather/seasonal/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seasonal_weather_by_attraction(self):
        SeasonalWeatherPattern.objects.create(
            attraction=self.attraction, season_type='dry',
            start_month=6, end_month=10, avg_temperature=18.0,
            avg_rainfall=5.0, description='Dry and cool.',
        )
        response = self.client.get('/api/v1/weather/seasonal/?attraction=kilimanjaro')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
