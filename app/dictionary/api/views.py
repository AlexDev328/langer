from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dictionary.api.serializers import LanguageSerializer, WordSerializer, WordCardSerializer, UserProfileSerializer, \
    WordCardSerializerDetail, CardGroupSerializer, WordSerializerInternal

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


class WordCardApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordCardSerializerDetail  # WordCardSerializer

    # permission_classes = (IsAuthenticated,)
    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardApiDetailViewGroup(WordCardApiDetailView):
    def perform_destroy(self, instance: WordCard):
        instance.card_groups.remove(self.kwargs['group_pk'])
        instance.save()
        if not instance.card_groups:
            instance.delete()


class CardGroupsListAPI(generics.ListCreateAPIView):
    serializer_class = CardGroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language_id']

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile)


class CardGroupsDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CardGroupSerializer

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile)


class CardGroupsCollectionAPI(generics.ListCreateAPIView):
    class WordCardSerializer(serializers.ModelSerializer):
        word = WordSerializerInternal()
        translation = WordSerializerInternal()
        score = serializers.SerializerMethodField()

        @transaction.atomic
        def create(self, validated_data):
            word_data = validated_data.pop('word')
            translation_data = validated_data.pop('translation')
            word, _ = Word.objects.get_or_create(**word_data)
            translation, _ = Word.objects.get_or_create(**translation_data)
            obj = super().create(word=word,
                                 translation=translation, owner=self.context.get('userprofile'),
                                 **validated_data)
            return obj

        @transaction.atomic
        def update(self, instance: WordCard, validated_data):

            if validated_data.get('word'):
                word_data = validated_data.pop('word')
                updated_word = WordSerializerInternal(instance=instance.word, data=word_data)
                if updated_word.is_valid():
                    updated_word.save()

            if validated_data.get('translation'):
                transation_data = validated_data.pop('translation')
                updated_translition = WordSerializerInternal(instance=instance.translation, data=transation_data)
                if updated_translition.is_valid():
                    updated_translition.save()

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance

        def get_score(self, obj):
            try:
                return WordCardProgress.objects.get(card=obj.id)
            except:
                return 0

        class Meta:
            model = WordCard
            exclude = ('owner', 'card_groups')

    serializer_class = WordCardSerializer

    def get_queryset(self):
        return WordCard.objects.filter(card_groups=self.kwargs['pk'])


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
