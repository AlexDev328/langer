from django.urls import path

from .views import LanguageApiView, WordApiView, WordCardApiView, WordCardsTrainingApiView
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
    path("trainings/simple", WordCardsTrainingApiView.as_view(), name='simple training')
]
