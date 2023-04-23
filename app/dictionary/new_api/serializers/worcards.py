from django.db import transaction
from rest_framework import serializers

from dictionary.models import Language, Word, CardGroup, WordCard, WordCardProgress


class WordSerializerInternal(serializers.ModelSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())

    class Meta:
        model = Word
        fields = ('text', 'language')

    def create(self, validated_data):
        language_data = validated_data.pop('language')
        instance = Word.objects.create(**validated_data, language=language_data)
        return instance

    @transaction.atomic
    def update(self, instance: Word, validated_data):
        language_data = validated_data.pop('language')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.language = language_data
        instance.save()
        return instance


class WordCardSerializer(serializers.ModelSerializer):
    word = WordSerializerInternal()
    translation = WordSerializerInternal()
    score = serializers.SerializerMethodField()
    card_groups = serializers.PrimaryKeyRelatedField(queryset=CardGroup.objects.all(), many=True,
                                                     required=False)  # write_only_true

    def validate(self, data):
        word_language = data['word']['language']
        card_group_language = data['card_groups'].language_id
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
        obj.card_groups.set(card_groups_data)
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
        exclude = ('owner', 'used_by', 'is_public')


class WordCardSerializerDetail(WordCardSerializer):
    score = serializers.SerializerMethodField(read_only=True)

    def get_score(self, obj):
        try:
            return WordCardProgress.objects.get(card=obj, owner=self.context['userprofile']).score
        except WordCardProgress.DoesNotExist:
            return 0
