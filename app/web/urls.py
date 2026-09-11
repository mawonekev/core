from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.home, name='home'),
    path('attractions/', views.attraction_list, name='attraction-list'),
    path('attractions/<slug:slug>/', views.attraction_detail, name='attraction-detail'),
    path('regions/', views.region_list, name='region-list'),
    path('regions/<slug:slug>/', views.region_detail, name='region-detail'),
    path('blog/', views.blog_list, name='blog-list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog-detail'),
    path('itineraries/', views.itineraries, name='itineraries'),
    path('itineraries/<slug:slug>/', views.itinerary_detail, name='itinerary-detail'),
    path('search/', views.search, name='search'),
    path('weather/', views.weather, name='weather'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('contributors/', views.contributors, name='contributors'),
    path('sponsor/', views.sponsor, name='sponsor'),
]
