from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Language(models.Model):
    name = models.CharField('Название', max_length=50)
    flag_code = models.CharField('Код', max_length=2, null=True)

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


class WordCard(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='слово или фраза', related_name='word_cards')
    translation = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='перевод', related_name='translation_cards')
    # объяснение перевода слова
    description = models.CharField('значение', max_length=300, null=True, blank=True)
    # примеры использования
    example = models.CharField("пример использования", max_length=300, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='создатель')
    is_public = models.BooleanField('доступна всем', default=True)

    def __str__(self):
        return f'{str(self.word)} - {str(self.translation)}'

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'карточки'


class CardGroup(models.Model):
    name = models.CharField('группа', max_length=300)
    cards = models.ManyToManyField(WordCard, verbose_name='карточки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель')
    is_public = models.BooleanField('доступна всем', default=False)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

    class Meta:
        verbose_name = 'подборка'
        verbose_name_plural = 'подборки'


class WordCardProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    card = models.ForeignKey(WordCard, on_delete=models.CASCADE, verbose_name='карточка')
    score = models.FloatField('процент правильных ответов [0..1]', default=0)
    count = models.IntegerField('количество тренировок', default=0)

    def __str__(self):
        return f"{self.user.username} - {str(self.card)}"

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогрессы'
