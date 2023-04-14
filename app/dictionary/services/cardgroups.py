from django.contrib.auth.models import User

from dictionary.models import CardGroup


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
