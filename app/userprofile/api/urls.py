from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from userprofile.api.views import UserProfileAPI

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profile/me", UserProfileAPI.as_view(), name='user profile')
]
