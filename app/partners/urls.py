from django.urls import path

from .views import partner_detail, partner_list_create

urlpatterns = [
    path('', partner_list_create, name='partner-list-create'),
    path('<slug:slug>/', partner_detail, name='partner-detail'),
]
