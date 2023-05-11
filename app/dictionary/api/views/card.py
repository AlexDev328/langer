from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from dictionary.api.filters import CardFilter
from dictionary.api.logical.views.service_based_apiview import ServiceListCreateApiView, \
    ServiceRetrieveUpdateDestroyApiView
from dictionary.api.paginations import StandardResultsSetPagination
from dictionary.api.permissions import CanAddCardToDeck
from dictionary.api.serializers.card import DeckCardSerializer, CardSerializer
from dictionary.models import Card
from dictionary.services.card import CardService


class CardsApi(ServiceListCreateApiView):
    permission_classes = (IsAuthenticated, CanAddCardToDeck)
    serializer_class = CardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CardFilter
    pagination_class = StandardResultsSetPagination
    service_class = CardService

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def get_serializer_context(self, **kwargs):
        context = super(CardsApi, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context


class CardApi(ServiceRetrieveUpdateDestroyApiView):
    serializer_class = CardSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, CanAddCardToDeck)
    service_class = CardService

    def get_queryset(self):
        return Card.objects.all()


class DeckCardApi(CardApi):
    serializer_class = DeckCardSerializer


