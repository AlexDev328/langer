from django.urls import path

from .views import LanguageApiView, WordApiView, WordCardApiView, WordCardsTrainingApiView, UserProfileAPI, \
    WordCardApiDetailView, WordCardProgressApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("languages", LanguageApiView.as_view(), name="languages"),
    path("words", WordApiView.as_view(), name="words"),
    path("wordcards", WordCardApiView.as_view(), name="words"),
    path("wordcards/<int:pk>", WordCardApiDetailView.as_view(), name="words"),
    path("trainings/simple", WordCardsTrainingApiView.as_view(), name='simple training'),
    path("trainings/simple/correct/<int:pk>", WordCardProgressApi.as_view(), name='training_results'),
    path("profile/me", UserProfileAPI.as_view(), name='user profile')
]
