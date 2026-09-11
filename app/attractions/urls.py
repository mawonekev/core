from django.urls import path

from app.feedback.views import attraction_reviews

from .views import (
    attraction_boundary,
    attraction_boundary_geojson,
    attraction_citations,
    attraction_detail,
    attraction_list_create,
    attraction_transport,
    attractions_by_category,
    attractions_by_region,
    attractions_nearby,
    attractions_within,
    citation_list,
    endemic_species_citations,
    endemic_species_list,
    featured_attractions,
    transport_by_type,
    transport_detail,
)

urlpatterns = [
    path('', attraction_list_create, name='attraction-list-create'),
    path('featured/', featured_attractions, name='attraction-featured'),
    path('by_category/', attractions_by_category, name='attraction-by-category'),
    path('by_region/', attractions_by_region, name='attraction-by-region'),
    path('within/', attractions_within, name='attractions-within'),
    path('nearby/', attractions_nearby, name='attractions-nearby'),
    path('citations/', citation_list, name='citation-list'),
    path('endemic-species/<int:pk>/citations/', endemic_species_citations, name='endemic-species-citations'),
    path('<slug:slug>/endemic-species/', endemic_species_list, name='attraction-endemic-species'),
    path('<slug:slug>/boundary/', attraction_boundary, name='attraction-boundary'),
    path('<slug:slug>/boundary/geojson/', attraction_boundary_geojson, name='attraction-boundary-geojson'),
    path('<slug:slug>/citations/', attraction_citations, name='attraction-citations'),
    path('<slug:slug>/reviews/', attraction_reviews, name='attraction-reviews'),
    path('<slug:slug>/transport/', attraction_transport, name='attraction-transport'),
    path('<slug:slug>/transport/filter/', transport_by_type, name='attraction-transport-filter'),
    path('transport/<int:pk>/', transport_detail, name='transport-detail'),
    path('<slug:slug>/', attraction_detail, name='attraction-detail'),
]
