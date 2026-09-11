from django.urls import path

from .views import article_detail, article_list_create

urlpatterns = [
    path('', article_list_create, name='article-list-create'),
    path('<slug:slug>/', article_detail, name='article-detail'),
]
