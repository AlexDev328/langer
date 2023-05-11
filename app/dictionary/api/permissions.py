from rest_framework.permissions import BasePermission


class CanAddCardToDeck(BasePermission):
    """
    Permission class to check if a user can add a card to a group.
    """

    def has_permission(self, request, view):
        decks = request.data.get('decks')
        if not decks:
            return True
        user_decks = request.user.userprofile.decks.values_list('id', flat=True)
        for deck_id in decks:
            if not user_decks.filter(pk=deck_id).exists():
                return False
        return True


