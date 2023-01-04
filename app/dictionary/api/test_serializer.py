from abc import ABC

from rest_framework.serializers import Serializer, ModelSerializer
from dictionary.models import Word, WordCard
from rest_framework import serializers


class WordCardTestSerializer(Serializer):
    text = serializers.CharField(source='word__text', default='Не сработало(')
    description = serializers.CharField(required=False, allow_null=True)
    example = serializers.CharField(required=False, allow_null=True)


class OptionTestSerializer(Serializer):
    text = serializers.CharField()


class WordCardsTrainingSerializer(Serializer):
    # TODO написать сериализатор на новый объект (слово, и 4 варианта ответа, и правильный ответ)
    wordcard = WordCardTestSerializer()
    options = OptionTestSerializer(many=True)


"""
from dictionary.api.test_serializer import *
a = Word.objects.filter(language_id=2)[:2].values('text')
b = WordCard.objects.select_related('word').values('word__text','description','example').first()
s = WordCardsTrainingSerializer(data = {'wordcard':b, 'options':list(a)})


b = WordCard.objects.select_related('word').values('word__text','description','example').first()
x = WordCardTestSerializer(data=b)

"""

