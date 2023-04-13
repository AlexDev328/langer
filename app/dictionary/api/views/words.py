from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from dictionary.api.serializers import WordSerializer
from dictionary.models import Word


class WordApiView(generics.ListCreateAPIView):
    serializer_class = WordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']

    def get_queryset(self):
        return Word.objects.all()