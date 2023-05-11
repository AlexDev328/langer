from rest_framework import serializers
from dictionary.api.serializers.language import LanguageSerializer
from dictionary.models import Word


class WordSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = Word
        fields = '__all__'
