from django.urls import path

from . import views

urlpatterns = [
    path('', views.announcement_list_create, name='announcement-list'),
    path('<int:pk>/', views.announcement_detail, name='announcement-detail'),
]
