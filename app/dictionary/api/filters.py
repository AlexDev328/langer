from django_filters import rest_framework as filters

from dictionary.models import WordCard


class WordCardFilter(filters.FilterSet):
    language = filters.NumberFilter(field_name='word__language')
    except_group = filters.NumberFilter(method='filter_by_group', label='Исключая группу')

    def filter_by_group(self, queryset, name, value):
        print(queryset.exclude(card_groups=value))
        return queryset.exclude(card_groups=value)

    class Meta:
        model = WordCard
        fields = ('language', 'except_group')
