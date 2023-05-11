from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from dictionary.api.serializers import DeckSerializer, WordSerializerInternal, DeckExpandSerializer, DeckCardSerializer
from dictionary.models import Deck, Card, CardProgress
from rest_framework import serializers
from dictionary.api.logical.views.service_based_apiview import ServiceListCreateApiView, \
    ServiceRetrieveUpdateDestroyApiView, ServiceUpdateApiView
from dictionary.api.paginations import StandardResultsSetPagination
from dictionary.api.permissions import CanAddCardToDeck
from dictionary.services.deck import DeckService, DeckDraftService
from dictionary.services.card import CardService


class DecksApi(ServiceListCreateApiView):
    serializer_class = DeckSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']
    pagination_class = StandardResultsSetPagination
    service_class = DeckService

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def perform_create(self, service):
        return service.save(owner=self.request.user.userprofile)


class DeckCardsApi(ServiceListCreateApiView):
    permission_classes = [IsAuthenticated, CanAddCardToDeck]
    pagination_class = StandardResultsSetPagination
    service_class = CardService
    serializer_class = DeckCardSerializer

    def get_queryset(self):
        return Card.objects.filter(decks=self.kwargs['pk'])


class DeckCardsApiPageable(DeckCardsApi):
    permission_classes = [IsAuthenticated, CanAddCardToDeck]
    pagination_class = StandardResultsSetPagination


class DeckDraftApi(ServiceUpdateApiView):
    serializer_class = DeckExpandSerializer
    service_class = DeckDraftService

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user.userprofile)


class DeckApi(ServiceRetrieveUpdateDestroyApiView):
    serializer_class = DeckSerializer

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user.userprofile)
