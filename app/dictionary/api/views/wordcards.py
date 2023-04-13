from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from dictionary.api.filters import WordCardFilter
from dictionary.api.paginations import StandardResultsSetPagination
from dictionary.api.permissions import CanAddCardToGroup
from dictionary.api.serializers.worcards import WordCardSerializer, WordCardSerializerDetail, WordSerializerInternal
from dictionary.models import WordCard, CardGroup, Word, WordCardProgress
from langer import settings


class WordCardApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, CanAddCardToGroup)
    serializer_class = WordCardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WordCardFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return WordCard.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context


class WordCardApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordCardSerializerDetail
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardApiDetailViewGroup(WordCardApiDetailView):
    class WordCardInGroupSerializer(serializers.ModelSerializer):
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
            except WordCardProgress.DoesNotExist:
                return 0

        class Meta:
            model = WordCard
            exclude = ('owner', 'used_by', 'is_public', 'card_groups')

    serializer_class = WordCardInGroupSerializer

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
            if not settings.DEBUG:
                instance.delete()
