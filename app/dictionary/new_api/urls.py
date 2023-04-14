from django.urls import path

from .views import LanguageApiView, WordApiView, WordCardApiView, \
    WordCardApiDetailView, CardGroupsListAPI, CardGroupsDetailAPI, CardGroupsCollectionAPI, WordCardApiDetailViewGroup, \
    CardGroupsExtendAPI, CardGroupsCollectionAPIPageable

urlpatterns = [

    path("languages", LanguageApiView.as_view(), name="languages"),
    path("words", WordApiView.as_view(), name="words"),

    path("cardgroups", CardGroupsListAPI.as_view(), name='cardgroups'),
    path("cardgroups/<int:pk>", CardGroupsDetailAPI.as_view(), name='cardgroups detail'),
    path("cardgroups/<int:pk>/expand", CardGroupsExtendAPI.as_view(), name='copy existing'),
    path("cardgroups/<int:pk>/card", CardGroupsCollectionAPI.as_view(), name='cardgroups wordcards'),
    path("cardgroups/<int:pk>/card/page", CardGroupsCollectionAPIPageable.as_view()),
    path("cardgroups/<int:group_pk>/card/<int:pk>", WordCardApiDetailViewGroup.as_view(), name="words"),

    path("wordcards", WordCardApiView.as_view(), name="words"),
    path("wordcards/<int:pk>", WordCardApiDetailView.as_view(), name="words"),
]
