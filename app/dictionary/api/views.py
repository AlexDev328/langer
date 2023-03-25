from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dictionary.api.serializers import LanguageSerializer, WordSerializer, WordCardSerializer, UserProfileSerializer, \
    WordCardSerializerDetail

from dictionary.models import Language, Word, WordCard, UserProfile, WordCardProgress, CardGroup


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

    def perform_create(self, serializer):
        with transaction.atomic():
            instance: WordCard = serializer.save()
            cg_id = self.request.data.get('card_group_id')
            cg: CardGroup = CardGroup.objects.get(id=cg_id)
            cg.cards.add(instance)


class WordCardApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordCardSerializerDetail  # WordCardSerializer

    # permission_classes = (IsAuthenticated,)
    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def perform_update(self, serializer):
        with transaction.atomic():
            old_instance:WordCard = self.get_object()
            print(old_instance.cardgroups)
            instance: WordCard = serializer.save()
            cg_id = self.request.data.get('card_group_id')
            cg: CardGroup = CardGroup.objects.get(id=cg_id)
            cg.cards.add(instance)

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
