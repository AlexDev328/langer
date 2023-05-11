from django_filters.rest_framework import DjangoFilterBackend

from dictionary.api.logical.views.service_based_apiview import ServiceListCreateApiView
from dictionary.api.serializers import WordSerializer
from dictionary.models import Word
from dictionary.services.word import WordService


class WordApiView(ServiceListCreateApiView):
    serializer_class = WordSerializer
    service_class = WordService
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']

    def get_queryset(self):
        return Word.objects.all()
