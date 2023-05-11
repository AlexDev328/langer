import random
from django.db import models
from django.db.models import Q

from userprofile.models import UserProfile


class Language(models.Model):
    name = models.CharField('Название', max_length=50)
    flag_code = models.CharField('Код', max_length=2, null=True)
    emoji = models.CharField('Эмоджи (для фронта)', max_length=4, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'язык'
        verbose_name_plural = 'языки'

    objects: models.Manager()


class Word(models.Model):
    text = models.CharField('Слово или фраза', max_length=150)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='язык')

    def __str__(self):
        return f'{self.text} ({self.language})'

    class Meta:
        verbose_name = 'cлово'
        verbose_name_plural = 'cлова'

    objects: models.Manager()


class ManagerCard(models.Manager):

    def get_training_set(self, language_id, user, size=5) -> list['Card']:
        cards = self.filter(Q(owner=user) | Q(used_by=user) & Q(word__language_id=language_id)).order_by('?')[:50]
        card_count = cards.count()
        if card_count < size:
            size = card_count
        cards = random.sample(list(cards), size)
        return cards

    def get_card_for_training(self, language_id, user, deck_id=None) -> 'Card':
        if deck_id:
            card = self.filter((Q(owner=user) | Q(used_by=user)) & Q(word__language_id=language_id) & Q(
                decks=deck_id)).order_by('?')[0]
        else:
            card = self.filter(Q(owner=user) | Q(used_by=user) & Q(word__language_id=language_id)).order_by('?')[0]
        return card

    def get_options_set(self, card, user, size=5) -> list[str]:
        cards = self.filter(
            (Q(owner=user) | Q(used_by=user)) & Q(word__language_id=card.word.language_id)).order_by(
            '?').values_list('translation__text', flat=True)
        card_count = cards.count()
        if card_count < size:
            size = card_count
        cards = random.sample(list(cards), size)
        return cards


class Card(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='слово или фраза', related_name='cards')
    transcription = models.CharField('транскрипция', max_length=255, blank=True, null=True)

    translation = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='перевод',
                                    related_name='translation_cards')
    # объяснение перевода слова
    description = models.CharField('значение', max_length=300, null=True, blank=True)
    # примеры использования
    example = models.CharField("пример использования", max_length=300, null=True, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, verbose_name='создатель',
                              related_name='cards')
    used_by = models.ManyToManyField(UserProfile, related_name='shared_cards', blank=True)
    is_public = models.BooleanField('доступна всем', default=False)
    decks = models.ManyToManyField('Deck', verbose_name='словарные группы', blank=True,
                                   related_name='cards')

    objects = models.Manager()
    training = ManagerCard()

    def __str__(self):
        return f'{str(self.word)} - {str(self.translation)}'

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'карточки'


class ManagerDeck(models.Manager):
    def get_training_set(self, user, size=5) -> list[Card]:
        cards = self.cards.filter(Q(owner=user) | Q(used_by=user)).order_by('?')[:50]
        card_count = cards.count()
        if card_count < size:
            size = card_count
        cards = random.sample(list(cards), size)
        return cards


class Deck(models.Model):
    name = models.CharField('группа', max_length=300)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name='создатель',
                              related_name='decks')
    used_by = models.ManyToManyField(UserProfile, related_name='shared_decks', blank=True)
    is_public = models.BooleanField('доступна всем', default=False)

    objects = models.Manager()
    training = ManagerDeck()

    @property
    def card_count(self):
        return self.cards.count()

    def __str__(self):
        return f"{self.name} "

    class Meta:
        verbose_name = 'колода'
        verbose_name_plural = 'колоды'


class CardProgress(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='карточка')
    score = models.IntegerField('знание словарной карточки (0..10)', default=0)

    objects: models.Manager()

    def __str__(self):
        return f"{self.owner.user.username if self.owner else ''} {self.card.word.text} - {self.score}"

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогрессы'
