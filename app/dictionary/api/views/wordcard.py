from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dictionary.api.filters import WordCardFilter
from dictionary.api.paginations import StandardResultsSetPagination
from dictionary.api.permissions import CanAddCardToGroup
from dictionary.api.logical.views import mixins
from dictionary.api.serializers.worcards import WordCardSerializer
from dictionary.models import WordCard
from dictionary.api.logical.views.service_based_apiview import ServiceListCreateAPIView, \
    ServiceRetrieveUpdateDestroyAPIView
from dictionary.services.wordcard import WordCardService


class WordCardApiView(ServiceListCreateAPIView):
    permission_classes = (IsAuthenticated, CanAddCardToGroup)
    serializer_class = WordCardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WordCardFilter
    pagination_class = StandardResultsSetPagination
    service_class = WordCardService

    def get_queryset(self):
        return WordCard.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context


class WordCardApiDetailView(ServiceRetrieveUpdateDestroyAPIView):
    serializer_class = WordCardSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, CanAddCardToGroup)
    service_class = WordCardService

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardApiDetailViewGroup(WordCardApiDetailView, mixins.CreateModelMixin):
    pass

