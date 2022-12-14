from django import forms

from .models import Word, WordCard, CardGroup, Language


class WordForm(forms.ModelForm):
    class Meta:
        model = WordCard
        fields = "__all__"


class FilterBard(forms.Form):
    text_language = forms.ModelChoiceField(Language.objects.all())


class WordCardCreate(forms.Form):
    text = forms.CharField(label='слово или фраза', max_length=150)
    text_language = forms.ModelChoiceField(Language.objects.all())
    translation = forms.CharField(label='перевод', max_length=150, required=False)
    translation_language = forms.ModelChoiceField(Language.objects.all(), required=False)
    description = forms.CharField(label='значение', max_length=150, required=False)
    example = forms.CharField(label="пример использования", max_length=300, required=False)
    group = forms.ModelChoiceField(CardGroup.objects.all(), required=False)
    is_public = forms.BooleanField(label='доступна всем', initial=True)


class TrainingSettings(forms.Form):
    language = forms.ModelChoiceField(Language.objects.all())
    task_count = forms.IntegerField(min_value=1)
