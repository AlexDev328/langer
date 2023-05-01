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
