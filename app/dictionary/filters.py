import django_filters

from app.dictionary.models import WordCard, Language


class WordCardFilter(django_filters.FilterSet):
    language = django_filters.ModelChoiceFilter(queryset=Language.objects.all(), field_name='word__language__name')

    class Meta:
        model = WordCard
        fields = ['language', 'id']