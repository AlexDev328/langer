from django.db import transaction
from rest_framework import serializers

from dictionary.models import Language, Word, Deck, Card, CardProgress


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


class CardSerializer(serializers.ModelSerializer):
    word = WordSerializerInternal()
    translation = WordSerializerInternal()
    score = serializers.SerializerMethodField(read_only=True)
    decks = serializers.PrimaryKeyRelatedField(queryset=Deck.objects.all(), many=True,
                                               required=False)  # write_only_true

    def validate(self, data):
        word_language = data['word']['language']
        if data.get('decks'):
            for deck in data.get('decks'):
                if word_language != deck.language:
                    raise serializers.ValidationError("Язык слова должен совпадать с языком колоды")
        return data

    def get_score(self, obj) -> int:
        try:
            return CardProgress.objects.get(card=obj.id, owner=self.context.get('request').user.userprofile).score
        except CardProgress.DoesNotExist:
            return 0

    class Meta:
        model = Card
        exclude = ('owner', 'used_by', 'is_public')


class DeckCardSerializer(CardSerializer):
    decks = None

    def validate(self, data):
        word_language = data['word']['language']
        card_group_language = Deck.objects.get(id=self.context['view'].kwargs['pk']).language
        if word_language != card_group_language:
            raise serializers.ValidationError("Язык слова должен совпадать с языком набора")
        return data

    class Meta:
        model = Card
        exclude = ('owner', 'used_by', 'is_public', 'decks')
