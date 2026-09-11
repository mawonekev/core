from django.urls import path

from .views import current_weather, forecast_weather, historical_weather, seasonal_weather, weather_detail, weather_list

urlpatterns = [
    path('', weather_list, name='weather-list'),
    path('<int:pk>/', weather_detail, name='weather-detail'),
    path('current/', current_weather, name='weather-current'),
    path('forecast/', forecast_weather, name='weather-forecast'),
    path('seasonal/', seasonal_weather, name='weather-seasonal'),
    path('historical/', historical_weather, name='weather-historical'),
]
