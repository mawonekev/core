from django.urls import path

from .views import operator_detail, operator_list_create, operators_by_attraction

urlpatterns = [
    path('', operator_list_create, name='operator-list-create'),
    path('by_attraction/', operators_by_attraction, name='operator-by-attraction'),
    path('<slug:slug>/', operator_detail, name='operator-detail'),
]
