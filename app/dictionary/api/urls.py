from django.urls import path

from .views import LanguageApiView, WordApiView, CardsApi, \
    CardApi, DeckApi, DeckCardsApi, DeckCardApi, \
    DeckDraftApi, DeckCardsApiPageable, DecksApi

urlpatterns = [

    path("languages", LanguageApiView.as_view(), name="languages"),
    path("words", WordApiView.as_view(), name="words"),

    path("decks", DecksApi.as_view(), name='decks'),
    path("decks/<int:pk>", DeckApi.as_view(), name='deck'),
    path("decks/<int:pk>/expand", DeckDraftApi.as_view(), name='draft card to deck'),
    path("decks/<int:pk>/card", DeckCardsApi.as_view(), name='deck cards'),
    path("decks/<int:pk>/card/page", DeckCardsApiPageable.as_view(), name='deck cards paged'),
    path("decks/<int:deck_pk>/card/<int:pk>", DeckCardApi.as_view(), name="deck card"),

    path("cards", CardsApi.as_view(), name="cards"),
    path("cards/<int:pk>", CardApi.as_view(), name="card"),
]
