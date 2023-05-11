from dictionary.models import Card
from dictionary.models import Deck
from dictionary.api.logical.services.base_service import BaseService


class DeckService(BaseService):
    model = Deck


class DeckDraftService(BaseService):
    model = Card

    def save(self, **kwargs):
        new_cards = set([i.id for i in self.data['cards']])
        old_cards = set(self.instance.cards.all().values_list('id', flat=True))
        self.instance.cards.set(old_cards | new_cards)
        return self.instance
