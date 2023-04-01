import random

from django.contrib.auth.models import User
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


class Word(models.Model):
    text = models.CharField('Слово или фраза', max_length=150)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='язык')

    def __str__(self):
        return f'{self.text} ({self.language})'

    class Meta:
        verbose_name = 'cлово'
        verbose_name_plural = 'cлова'


class ManagerWordCard(models.Manager):
    def get_random_words(self, owner_id, language_id: Language, except_id=None, count: int = 2) -> list['WordCard']:
        query = super(models.Manager, self).get_queryset().filter(
            (Q(owner_id=owner_id) | Q(is_public=True)) & Q(word__language_id=language_id) & ~Q(id=except_id)).order_by(
            'id')
        random_words = random.choices(query, k=count)
        return random_words

    def get_options_for_wordcard(self, user_id, wordcard: 'WordCard', count: int = 2):
        query = super(models.Manager, self).get_queryset().filter(
            (Q(owner_id=user_id) | Q(is_public=True)) &
            Q(word__language_id=wordcard.word.language_id) &
            ~Q(id=wordcard.id)
        ).order_by('id').values_list('translation__text', flat=True)

        random_words = random.choices(query, k=count)

        return random_words


class WordCard(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='слово или фраза', related_name='word_cards')
    transcription = models.CharField('транскрипция', max_length=255, blank=True, null=True)

    translation = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='перевод',
                                    related_name='translation_cards')
    # объяснение перевода слова
    description = models.CharField('значение', max_length=300, null=True, blank=True)
    # примеры использования
    example = models.CharField("пример использования", max_length=300, null=True, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, verbose_name='создатель')
    is_public = models.BooleanField('доступна всем', default=True)
    card_groups = models.ManyToManyField('CardGroup', verbose_name='словарные группы', blank=True)

    objects = ManagerWordCard()

    def __str__(self):
        return f'{str(self.word)} - {str(self.translation)}'

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'карточки'


class CardGroup(models.Model):
    name = models.CharField('группа', max_length=300)
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='создатель')
    is_public = models.BooleanField('доступна всем', default=False)

    @property
    def card_count(self):
        return self.wordcard_set.count()

    @property
    def card_learned(self):
        return self.wordcard_set.filter(wordcardprogress__score=1).count()

    def __str__(self):
        return f"{self.name} ({self.owner.user.username})"

    class Meta:
        verbose_name = 'подборка'
        verbose_name_plural = 'подборки'


class WordCardProgress(models.Model):
    card = models.ForeignKey(WordCard, on_delete=models.CASCADE, verbose_name='карточка')
    score = models.IntegerField('знание словарной карточки (0..10)', default=0)

    def __str__(self):
        return f"{self.card.owner} {self.card.word.text} - {self.score}"

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогрессы'



