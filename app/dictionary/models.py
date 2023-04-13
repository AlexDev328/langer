import random
from django.db import models
from django.db.models import Q

from userprofile.models import UserProfile


class Language(models.Model):
    name = models.CharField('Название', max_length=50)
    flag_code = models.CharField('Код', max_length=2, null=True)
    emoji = models.CharField('Эмоджи (для фронта)', max_length=3, null=True, blank=True)

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


class ManagerWordCard(models.Manager):

    def get_training_set(self, language_id, user, size=5) -> list['WordCard']:
        cards = self.filter(Q(owner=user) | Q(used_by=user) & Q(word__language_id=language_id)).order_by('?')[:50]
        cards_count = cards.count()
        if cards_count < size:
            size = cards_count
        cards = random.sample(list(cards), size)
        return cards

    def get_wordcard_for_training(self, language_id, user, cardgroup_id=None) -> 'WordCard':
        if cardgroup_id:
            card = self.filter((Q(owner=user) | Q(used_by=user)) & Q(word__language_id=language_id) & Q(
                card_groups=cardgroup_id)).order_by('?')[0]
        else:
            card = self.filter(Q(owner=user) | Q(used_by=user) & Q(word__language_id=language_id)).order_by('?')[0]
        return card

    def get_options_set(self, wordcard, user, size=5) -> list[str]:
        cards = self.filter(
            (Q(owner=user) | Q(used_by=user)) & Q(word__language_id=wordcard.word.language_id)).order_by(
            '?').values_list('translation__text', flat=True)
        cards_count = cards.count()
        if cards_count < size:
            size = cards_count
        cards = random.sample(list(cards), size)
        return cards


class WordCard(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='слово или фраза', related_name='word_cards')
    transcription = models.CharField('транскрипция', max_length=255, blank=True, null=True)

    translation = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='перевод',
                                    related_name='translation_cards')
    # объяснение перевода слова
    description = models.CharField('значение', max_length=300, null=True, blank=True)
    # примеры использования
    example = models.CharField("пример использования", max_length=300, null=True, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, verbose_name='создатель',
                              related_name='wordcards')
    used_by = models.ManyToManyField(UserProfile, related_name='shared_wordcards', blank=True)
    is_public = models.BooleanField('доступна всем', default=False)
    card_groups = models.ManyToManyField('CardGroup', verbose_name='словарные группы', blank=True,
                                         related_name='wordcards')

    objects = models.Manager()
    training = ManagerWordCard()

    def __str__(self):
        return f'{str(self.word)} - {str(self.translation)}'

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'карточки'


class ManagerCardGroup(models.Manager):
    def get_training_set(self, user, size=5) -> list[WordCard]:
        cards = self.wordcards.filter(Q(owner=user) | Q(used_by=user)).order_by('?')[:50]
        cards_count = cards.count()
        if cards_count < size:
            size = cards_count
        cards = random.sample(list(cards), size)
        return cards


class CardGroup(models.Model):
    name = models.CharField('группа', max_length=300)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name='создатель',
                              related_name='card_groups')
    used_by = models.ManyToManyField(UserProfile, related_name='shared_cardgroups', blank=True)
    is_public = models.BooleanField('доступна всем', default=False)

    objects = models.Manager()
    training = ManagerCardGroup()

    @property
    def card_count(self):
        return self.wordcards.count()

    def __str__(self):
        return f"{self.name} "

    class Meta:
        verbose_name = 'подборка'
        verbose_name_plural = 'подборки'


class WordCardProgress(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(WordCard, on_delete=models.CASCADE, verbose_name='карточка')
    score = models.IntegerField('знание словарной карточки (0..10)', default=0)

    objects: models.Manager()

    def __str__(self):
        return f"{self.owner.user.username if self.owner else ''} {self.card.word.text} - {self.score}"

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогрессы'
