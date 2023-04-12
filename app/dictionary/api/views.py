from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dictionary.api.filters import WordCardFilter
from dictionary.api.permissions import CanAddCardToGroup
from dictionary.api.serializers import LanguageSerializer, WordSerializer, WordCardSerializer, \
    WordCardSerializerDetail, CardGroupSerializer, WordSerializerInternal

from dictionary.models import Language, Word, WordCard, WordCardProgress, CardGroup


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50


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
    permission_classes = [IsAuthenticated, CanAddCardToGroup]
    serializer_class = WordCardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WordCardFilter
    pagination_class = StandardResultsSetPagination

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WordCard.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context


class WordCardApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordCardSerializerDetail
    pagination_class = StandardResultsSetPagination

    # WordCardSerializer

    # permission_classes = (IsAuthenticated,)
    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardApiDetailViewGroup(WordCardApiDetailView):
    class WordCardSerializer(serializers.ModelSerializer):
        word = WordSerializerInternal()
        translation = WordSerializerInternal()
        score = serializers.SerializerMethodField()

        # card_groups = serializers.PrimaryKeyRelatedField(queryset=CardGroup.objects.all(), many=True, write_only=True)

        def validate(self, data):
            word_language = data['word']['language']

            card_group_language = CardGroup.objects.get(id=self.context['view'].kwargs['group_pk']).language_id
            if word_language != card_group_language:
                raise serializers.ValidationError("Язык слова должен совпадать с языком набора")
            return data

        @transaction.atomic
        def create(self, validated_data):
            word_data = validated_data.pop('word')
            translation_data = validated_data.pop('translation')
            card_groups_data = validated_data.pop('card_groups', [])

            word, _ = Word.objects.get_or_create(**word_data)

            translation, _ = Word.objects.get_or_create(**translation_data)

            obj = WordCard.objects.create(
                word=word,
                translation=translation,
                owner=self.context.get('userprofile'),
                **validated_data
            )
            obj.card_groups.add(self.context['view'].kwargs['pk'])
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
                return WordCardProgress.objects.get(card=obj.id, owner=self.context['userprofile']).score
            except:
                return 0

        class Meta:
            model = WordCard
            exclude = ('owner', 'used_by', 'is_public', 'card_groups')

    serializer_class = WordCardSerializer

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def get_queryset(self):
        return WordCard.objects.all()

    def perform_destroy(self, instance: WordCard):
        instance.card_groups.remove(self.kwargs['group_pk'])
        instance.save()
        if not instance.card_groups.exists():
            print('удаляем карточку')
            # instance.delete()


class CardGroupsListAPI(generics.ListCreateAPIView):
    serializer_class = CardGroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.userprofile)


class CardGroupsDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CardGroupSerializer

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile)


class CardGroupsExtendAPI(generics.UpdateAPIView):
    class CardGroupExpandSerializer(serializers.ModelSerializer):
        wordcards = serializers.PrimaryKeyRelatedField(many=True, queryset=WordCard.objects.all())

        class Meta:
            model = CardGroup
            fields = ('wordcards',)

        def update(self, instance, validated_data):
            new = set([i.id for i in validated_data['wordcards']])
            old = set(instance.wordcards.all().values_list('id', flat=True))
            instance.wordcards.set(old | new)
            return instance

    serializer_class = CardGroupExpandSerializer

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile)


class CardGroupsCollectionAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, CanAddCardToGroup]
    pagination_class = StandardResultsSetPagination

    class WordCardSerializer(serializers.ModelSerializer):
        word = WordSerializerInternal()
        translation = WordSerializerInternal()
        score = serializers.SerializerMethodField()

        # card_groups = serializers.PrimaryKeyRelatedField(queryset=CardGroup.objects.all(), many=True, write_only=True)

        def validate(self, data):
            word_language = data['word']['language']

            card_group_language = CardGroup.objects.get(id=self.context['view'].kwargs['pk']).language
            if word_language != card_group_language:
                raise serializers.ValidationError("Язык слова должен совпадать с языком набора")
            return data

        @transaction.atomic
        def create(self, validated_data):
            word_data = validated_data.pop('word')
            translation_data = validated_data.pop('translation')
            card_groups_data = validated_data.pop('card_groups', [])

            word, _ = Word.objects.get_or_create(**word_data)

            translation, _ = Word.objects.get_or_create(**translation_data)

            obj = WordCard.objects.create(
                word=word,
                translation=translation,
                owner=self.context.get('userprofile'),
                **validated_data
            )
            obj.card_groups.add(self.context['view'].kwargs['pk'])
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
                return WordCardProgress.objects.get(card=obj.id).score
            except:
                return 0

        class Meta:
            model = WordCard
            exclude = ('owner', 'used_by', 'is_public', 'card_groups')

    serializer_class = WordCardSerializer

    def get_queryset(self):
        return WordCard.objects.filter(card_groups=self.kwargs['pk'])


class CardGroupsCollectionAPIPageable(CardGroupsCollectionAPI):
    # permission_classes = [IsAuthenticated, CanAddCardToGroup]
    pagination_class = StandardResultsSetPagination


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
