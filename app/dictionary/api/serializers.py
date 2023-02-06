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


class WordSerializerInternal(serializers.ModelSerializer):
    language_id = serializers.IntegerField()
    class Meta:
        model = Word
        fields = ('text', 'language_id')

    def create(self, validated_data):
        language_data = validated_data.pop('language_id')
        instance = Word.objects.create(**validated_data, language_id=language_data)
        return instance

    def update(self, instance: Word, validated_data):
        language_data = validated_data.pop('language_id')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.language_id = language_data
        instance.save()
        return instance


class WordCardSerializer(serializers.ModelSerializer):
    word = WordSerializerInternal()
    translation = WordSerializerInternal()

    def create(self, validated_data):
        print(validated_data)
        word_data = validated_data.pop('word')
        transation_data = validated_data.pop('translation')
        word, _ = Word.objects.get_or_create(**word_data)
        translition, _ = Word.objects.get_or_create(**transation_data)
        return WordCard.objects.create(word=word,
                                       translation=translition, owner=self.context.get('userprofile'),
                                       **validated_data)

    def update(self, instance: WordCard, validated_data):
        print(validated_data)
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

    class Meta:
        model = WordCard
        exclude = ('owner',)


class WordCardSerializerDetail(WordCardSerializer):
    score = serializers.SerializerMethodField(read_only=True)

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
