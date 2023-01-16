from rest_framework import serializers

from dictionary.models import Language, WordCard, CardGroup, WordCardProgress, Word, UserProfile


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = Word
        fields = '__all__'


class WordSerializerS(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class WordCardSerializer(serializers.ModelSerializer):
    word = WordSerializerS()
    translation = WordSerializerS()

    def create(self, validated_data):
        print(validated_data)
        word_data = validated_data.pop('word')
        transation_data = validated_data.pop('translation')
        word, _ = Word.objects.get_or_create(**word_data)
        translition, _ = Word.objects.get_or_create(**transation_data)
        return WordCard.objects.create(word=word,
                                       translation=translition, owner=self.context.get('request').user,
                                       **validated_data)

    class Meta:
        model = WordCard
        exclude = ('owner',)


class WordCardSerializerDetail(WordCardSerializer):
    score = serializers.SerializerMethodField()

    def get_score(self, obj):
        profile = self.context.get('userprofile')
        try:
            return WordCardProgress.objects.get(user_id=profile.id, card=obj).score
        except WordCardProgress.DoesNotExist:
            return 0


class CardGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardGroup
        fields = '__all__'


class WordCardProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordCardProgress
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'default_language')
