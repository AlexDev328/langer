from rest_framework.serializers import Serializer
from rest_framework import serializers


class WordCardTestSerializer(Serializer):
    id = serializers.IntegerField(source='pk')
    text = serializers.CharField(source='word.text')
    description = serializers.CharField(required=False, allow_null=True)
    example = serializers.CharField(required=False, allow_null=True)
    translation = serializers.CharField(source='translation.text')


class OptionTestSerializer(Serializer):
    text = serializers.CharField(source='translation.text')


class WordCardsTrainingSerializer(Serializer):
    # TODO написать сериализатор на новый объект (слово, и 4 варианта ответа, и правильный ответ)
    wordcard = WordCardTestSerializer(read_only=True)
    options = serializers.ListSerializer(child=serializers.CharField())#serializers.CharField(many=True)#OptionTestSerializer(many=True, read_only=True)

