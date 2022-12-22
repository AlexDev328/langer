from rest_framework import serializers

from dictionary.models import Language, WordCard, CardGroup, WordCardProgress, Word


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    class Meta:
        model = Word
        fields = '__all__'


class WordCardSerializer(serializers.ModelSerializer):
    word = WordSerializer()
    translation = WordSerializer()

    def create(self, validated_data):
        print(validated_data)
        word_data = validated_data.pop('word')
        transation_data = validated_data.pop('translation')
        word, _ = Word.objects.get_or_create(**word_data)
        translition, _ = Word.objects.get_or_create(**transation_data)
        return WordCard.objects.create(word=word,
                                       translation=translition, owner=self.context.get('request').user, **validated_data)

    class Meta:
        model = WordCard
        exclude = ('owner',)


class CardGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardGroup
        fields = '__all__'


class WordCardProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordCardProgress
        fields = '__all__'
