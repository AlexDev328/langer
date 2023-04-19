from django.db import models

from dictionary.models import Language


# Create your models here.


class Letter(models.Model):
    symbol = models.CharField('Символ', max_length=10)
    transcription = models.CharField('транскрипция', max_length=10)  # транслитерация
    language = models.ForeignKey(Language, on_delete=models.RESTRICT, verbose_name='язык')

    def __str__(self):
        return self.symbol


class Alphabet(models.Model):
    name = models.CharField('Название', max_length=20)
    one_dimension = models.BooleanField(default=True)
    language = models.ForeignKey(Language, on_delete=models.RESTRICT, verbose_name='язык')


class AlphabetEntry(models.Model):
    alphabet = models.ForeignKey(Alphabet, on_delete=models.RESTRICT, verbose_name='алфавит')
    letter = models.ForeignKey(Letter, on_delete=models.RESTRICT, verbose_name='язык')
    lang_index_column = models.IntegerField()
    lang_index_row = models.IntegerField(blank=True, null=True)

    # может валидация заполнения второго измерения


class LetterGroup(models.Model):
    name = models.CharField('Название', max_length=50)
    letters = models.ManyToManyField(Letter)

    def __str__(self):
        return self.name
