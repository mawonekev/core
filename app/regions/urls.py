from django.urls import path

from .views import region_detail, region_list_create

urlpatterns = [
    path('', region_list_create, name='region-list-create'),
    path('<slug:slug>/', region_detail, name='region-detail'),
]
