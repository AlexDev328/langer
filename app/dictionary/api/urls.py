from django.urls import path

from .views import LanguageApiView, WordApiView, WordCardApiView, UserProfileAPI, \
    WordCardApiDetailView, CardGroupsListAPI, CardGroupsDetailAPI, CardGroupsCollectionAPI, WordCardApiDetailViewGroup
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("languages", LanguageApiView.as_view(), name="languages"),
    path("words", WordApiView.as_view(), name="words"),
    path("cardgroups", CardGroupsListAPI.as_view(), name='cardgroups'),
    path("cardgroups/<int:pk>/edit", CardGroupsDetailAPI.as_view(), name='cardgroups detail'),
    path("cardgroups/<int:pk>", CardGroupsCollectionAPI.as_view(), name='cardgroups wordcards'),
    path("cardgroups/<int:group_pk>/card/<int:pk>", WordCardApiDetailViewGroup.as_view(), name="words"),

    path("wordcards", WordCardApiView.as_view(), name="words"),
    path("wordcards/<int:pk>", WordCardApiDetailView.as_view(), name="words"),
    path("profile/me", UserProfileAPI.as_view(), name='user profile')
]
