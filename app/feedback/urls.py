from django.urls import path

from .views import attraction_reviews, review_detail, submit_feedback

urlpatterns = [
    path('submit/', submit_feedback, name='submit-feedback'),
    path('attractions/<slug:slug>/reviews/', attraction_reviews, name='attraction-reviews'),
    path('reviews/<int:pk>/', review_detail, name='review-detail'),
]
