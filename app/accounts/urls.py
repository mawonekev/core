from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import login, register, resend_verification, user_profile, verify_email

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', user_profile, name='user_profile'),
    path('verify-email/', verify_email, name='verify_email'),
    path('resend-verification/', resend_verification, name='resend_verification'),
]
