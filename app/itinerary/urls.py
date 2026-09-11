from django.urls import path

from .views import add_activity, itinerary_days, itinerary_detail, itinerary_list_create

urlpatterns = [
    path('', itinerary_list_create, name='itinerary-list'),
    path('<slug:slug>/', itinerary_detail, name='itinerary-detail'),
    path('<slug:slug>/days/', itinerary_days, name='itinerary-days'),
    path('days/<int:day_id>/activities/', add_activity, name='itinerary-add-activity'),
]
