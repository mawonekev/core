from django.urls import path

from .views import media_detail, media_list_create

urlpatterns = [
    path('', media_list_create, name='media-list'),
    path('<int:pk>/', media_detail, name='media-detail'),
]
