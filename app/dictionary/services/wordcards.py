from django.contrib.auth.models import User
from django.db import transaction

from dictionary.api.serializers import WordSerializerInternal
from dictionary.models import WordCard, Word
from dictionary.new_api.logical.services.base_service import BaseService
from dictionary.services.word import WordService


def process_update_wordcard(instance: WordCard, user: User, update_data: dict):
    if update_data.get('card_groups'):
        # check ownership on card_groups
        pass


class WordCardService(BaseService):
    model = WordCard

    @transaction.atomic
    def create(self, **kwargs):
        validated_data = self.data
        word_data = validated_data.pop('word')
        translation_data = validated_data.pop('translation')

        word, _ = Word.objects.get_or_create(**word_data)

        translation, _ = Word.objects.get_or_create(**translation_data)

        obj = WordCard.objects.create(
            word=word,
            translation=translation,
            owner=self.context.get('userprofile'),
            **validated_data
        )
        obj.card_groups.add(self.context['view'].kwargs['pk'])
        return obj

    @transaction.atomic
    def update(self, instance: WordCard, validated_data):

        if validated_data.get('word'):
            word_data = validated_data.pop('word')
            updated_word = WordSerializerInternal(instance=instance.word, data=word_data)
            if updated_word.is_valid():
                word_service = WordService(updated_word)
                word_service.is_valid()
                word_service.update()

        if validated_data.get('translation'):
            transation_data = validated_data.pop('translation')
            updated_translition = WordSerializerInternal(instance=instance.translation, data=transation_data)
            if updated_translition.is_valid():
                word_service = WordService(updated_translition)
                word_service.is_valid()
                word_service.update()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
