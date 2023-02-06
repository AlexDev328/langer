from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer, Serializer
from rest_framework.views import APIView

from dictionary.api.serializers import LanguageSerializer, WordSerializer, WordCardSerializer, UserProfileSerializer, \
    WordCardSerializerDetail
from dictionary.api.test_serializer import WordCardsTrainingSerializer

from dictionary.models import Language, Word, WordCard, UserProfile, WordCardProgress


class UserProfileAPI(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        instance = UserProfile.objects.get(user=self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordCardSerializerDetail  # WordCardSerializer

    # permission_classes = (IsAuthenticated,)
    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    '''def get_serializer_class(self):
        if self.request.method == "GET":
            return WordCardSerializerDetail
        else:
            return WordCardSerializer'''

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardProgressApi(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        if "correct" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            progress, _ = WordCardProgress.objects.get_or_create(user=self.request.user.userprofile,
                                                                 card_id=kwargs['pk'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.data['correct']:
            progress.score += 1
        else:
            progress.score -= 1
        progress.save()
        return Response(status=status.HTTP_201_CREATED)


class TrainingCheckApiView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        print(request)
        try:
            progress, _ = WordCardProgress.objects.get_or_create(user=self.request.user.userprofile,
                                                                 card_id=kwargs['pk'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.data['answer'] == WordCard.objects.get(id=kwargs['pk']).translation.text:
            progress.score += 1
            progress.save()
            return Response(status=status.HTTP_200_OK, data={'right_answer': WordCard.objects.get(id=kwargs['pk']).translation.text,'correct': True})
        return Response(status=status.HTTP_200_OK,
                        data={'right_answer': WordCard.objects.get(id=kwargs['pk']).translation.text, 'correct': False})


class WordCardsTrainingApiView(generics.RetrieveUpdateAPIView):
    serializer_class = WordCardsTrainingSerializer

    def get(self, request, *args, **kwargs):
        print(request)
        word = WordCard.objects.get_random_words(user_id=request.user.id, language_id=2, count=1)[0]
        options = WordCard.objects.get_options_for_wordcard(user_id=request.user.id, wordcard=word,
                                                            count=3)
        serializer = WordCardsTrainingSerializer({'wordcard': word, 'options': list(options)})
        return Response(serializer.data)
