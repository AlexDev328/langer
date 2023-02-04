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
    language = serializers.IntegerField(source='language_id')

    class Meta:
        model = Word
        fields = ('text', 'language')

    def create(self, validated_data):
        language_data = validated_data.pop('language')
        l_serializer = LanguageSerializer(data=language_data)
        if l_serializer.is_valid(raise_exception=True):
            language = l_serializer.save()
        instance = self.save(language=language)
        return instance

    def update(self, instance, validated_data):
        language_data = validated_data.pop('language')
        l_serializer = LanguageSerializer(instance.language, language_data)
        if l_serializer.is_valid(raise_exception=True):
            language = l_serializer.save()
        instance = self.save(language=language)
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
        word_data = validated_data.pop('word')
        # word_data['language_id'] = word_data.pop('language')
        transation_data = validated_data.pop('translation')
        # transation_data['language_id'] = transation_data.pop('language')
        updated_word = WordSerializerInternal(instance=instance.word, data=word_data)
        if updated_word.is_valid():
            updated_word.save()
        print(updated_word.errors)
        updated_translition = WordSerializerInternal(instance=instance.translation, data=transation_data)
        if updated_translition.is_valid(raise_exception=True):
            updated_translition.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
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
