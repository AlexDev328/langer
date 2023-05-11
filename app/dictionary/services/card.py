from django.contrib.auth.models import User
from django.db import transaction

from dictionary.api.serializers import WordSerializerInternal
from dictionary.models import Card, Word
from dictionary.api.logical.services.base_service import BaseService
from dictionary.services.word import WordService
from langer import settings


class CardService(BaseService):
    model = Card

    def get_decks_for_create(self, validated_data):
        if validated_data.get('decks') is None:
            return self.context['view'].kwargs.get('deck_pk', None)  # TODO Check
        return validated_data.pop('decks')

    def get_decks_for_update(self, validated_data):
        if validated_data.get('decks') is not None:
            return validated_data.pop('decks')
        return None

    @transaction.atomic
    def create(self, **kwargs):
        validated_data = self.data
        word_data = validated_data.pop('word')
        translation_data = validated_data.pop('translation')

        word, _ = Word.objects.get_or_create(**word_data)

        translation, _ = Word.objects.get_or_create(**translation_data)

        decks_to_save = self.get_decks_for_create(validated_data)

        obj = Card.objects.create(
            word=word,
            translation=translation,
            owner=self.context.get('userprofile'),
            **validated_data
        )

        if decks_to_save:
            not_owned = obj.decks.exclude(owner=obj.owner).values_list('id', flat=True)
            obj.decks.set(set(not_owned) | set(decks_to_save))

        return obj

    @transaction.atomic
    def update(self):
        self.update_word(self.data, 'word')
        self.update_word(self.data, 'translation')

        decks_to_save = self.get_decks_for_update(self.data)

        for attr, value in self.data.items():
            setattr(self.instance, attr, value)

        if decks_to_save:
            self.instance.decks.set(decks_to_save)

        self.instance.save()
        return self.instance

    def update_word(self, validated_data, key='word'):
        if not validated_data.get(key):
            return
        word_data = validated_data.pop(key)
        updated_word = WordSerializerInternal(instance=getattr(self.instance, key), data=word_data)
        if not updated_word.is_valid():
            raise Exception
        word_service = WordService(updated_word)
        word_service.is_valid()
        word, created = word_service.get_or_create()
        setattr(self.instance, key, word)


class DeckCardService(CardService):
    @transaction.atomic
    def update(self):
        if self.instance.owner != self.context['userprofile']:
            return self.create()
        else:
            return super().update()

    def destroy(self, **kwargs):
        self.instance.decks.remove(self.context['request'].kwargs['deck_pk'])
        self.instance.save()
        if not self.instance.decks.exists():
            print('удаляем карточку')
            if not settings.DEBUG:
                self.instance.delete()
