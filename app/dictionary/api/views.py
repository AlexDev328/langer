from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer, Serializer

from dictionary.api.serializers import LanguageSerializer, WordSerializer, WordCardSerializer
from dictionary.api.test_serializer import WordCardsTrainingSerializer

from dictionary.models import Language, Word, WordCard


class LanguageApiView(generics.ListCreateAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class WordApiView(generics.ListCreateAPIView):
    serializer_class = WordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']

    def get_queryset(self):
        return Word.objects.all()


class WordCardApiView(generics.ListCreateAPIView):
    serializer_class = WordCardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['word__language']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardsTrainingApiView(generics.RetrieveUpdateAPIView):

    def get(self, request, *args, **kwargs):
        print(request)
        word = WordCard.objects.get_random_words(user_id=request.user.id, language_id=2, count=1)[0]
        options = WordCard.objects.get_random_words(user_id=request.user.id, language_id=2, count=3)
        serializer = WordCardsTrainingSerializer({'wordcard': word, 'options': list(options)})
        return Response(serializer.data)
