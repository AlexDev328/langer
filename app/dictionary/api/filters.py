from django_filters import rest_framework as filters

from dictionary.models import Card


class CardFilter(filters.FilterSet):
    language = filters.NumberFilter(field_name='word__language')
    except_deck = filters.NumberFilter(method='filter_by_deck', label='Исключая группу')

    def filter_by_deck(self, queryset, name, value):
        print(queryset.exclude(decks=value))
        return queryset.exclude(decks=value)

    class Meta:
        model = Card
        fields = ('language', 'except_deck')
