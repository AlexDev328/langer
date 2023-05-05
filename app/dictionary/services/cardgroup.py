from django.contrib.auth.models import User

from dictionary.models import CardGroup, WordCard, Word


def check_ownership_on_group(card_group: int, user: User):
    try:
        CardGroup.objects.get(id=card_group, owner=user.profile)
    except CardGroup.DoesNotExist:
        return False
    return True


def check_ownership_on_groups(card_groups: list, user):
    try:
        for i in card_groups:
            CardGroup.objects.get(id=i, owner=user.profile)
    except CardGroup.DoesNotExist:
        return False
    return True


from dictionary.models import CardGroup
from dictionary.api.logical.services.base_service import BaseService


class CardGroupService(BaseService):
    model = CardGroup


class CardGroupExpandingService(BaseService):
    model = WordCard

    def save(self, **kwargs):
        new = set([i.id for i in self.data['wordcards']])
        old = set(self.instance.wordcards.all().values_list('id', flat=True))
        self.instance.wordcards.set(old | new)
        return self.instance
