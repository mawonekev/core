from django.urls import path

from .views import contributor_detail, contributor_list, profile_update

urlpatterns = [
    path('', contributor_list, name='contributor-list'),
    path('me/update/', profile_update, name='profile-update'),
    path('<str:username>/', contributor_detail, name='contributor-detail'),
]
