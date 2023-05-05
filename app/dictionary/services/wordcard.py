from django.contrib.auth.models import User
from django.db import transaction

from dictionary.api.serializers import WordSerializerInternal
from dictionary.models import WordCard, Word
from dictionary.api.logical.services.base_service import BaseService
from dictionary.services.word import WordService
from langer import settings


def process_update_wordcard(instance: WordCard, user: User, update_data: dict):
    if update_data.get('card_groups'):
        # check ownership on card_groups
        pass


class WordCardService(BaseService):
    model = WordCard

    def get_card_groups_for_create(self, validated_data):
        if validated_data.get('card_groups') is None:
            return self.context['view'].kwargs.get('pk', None)  # TODO Check
        return validated_data.pop('card_groups')

    def get_card_groups_for_update(self, validated_data):
        if validated_data.get('card_groups') is not None:
            return validated_data.pop('card_groups')
        return None

    @transaction.atomic
    def create(self, **kwargs):
        validated_data = self.data
        word_data = validated_data.pop('word')
        translation_data = validated_data.pop('translation')

        word, _ = Word.objects.get_or_create(**word_data)

        translation, _ = Word.objects.get_or_create(**translation_data)

        card_groups_to_save = self.get_card_groups_for_create(validated_data)

        obj = WordCard.objects.create(
            word=word,
            translation=translation,
            owner=self.context.get('userprofile'),
            **validated_data
        )

        if card_groups_to_save:
            not_owned = obj.card_groups.exclude(owner=obj.owner).values_list('id', flat=True)
            obj.card_groups.set(*not_owned, *card_groups_to_save)

        return obj

    @transaction.atomic
    def update(self):
        self.update_word(self.data, 'word')
        self.update_word(self.data, 'translation')

        card_groups_to_save = self.get_card_groups_for_update(self.data)

        for attr, value in self.data.items():
            setattr(self.instance, attr, value)

        if card_groups_to_save:
            self.instance.card_groups.set(card_groups_to_save)

        self.instance.save()
        return self.instance

    def update_word(self, validated_data, key='word'):
        if not validated_data.get(key):
            return
        word_data = validated_data.pop(key)
        updated_word = WordSerializerInternal(instance=getattr(self.instance, key), data=word_data)
        if not updated_word.is_valid():
            return
        word_service = WordService(updated_word)
        word_service.is_valid()
        word, created = word_service.get_or_create()
        setattr(self.instance, key, word)


class WordCardInGroupService(WordCardService):
    @transaction.atomic
    def update(self):
        if self.instance.owner != self.context['userprofile']:
            return self.create()
        else:
            return super().update()

    def destroy(self, **kwargs):
        self.instance.card_groups.remove(self.context['request'].kwargs['group_pk'])
        self.instance.save()
        if not self.instance.card_groups.exists():
            print('удаляем карточку')
            if not settings.DEBUG:
                self.instance.delete()
