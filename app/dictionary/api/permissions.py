from rest_framework.permissions import BasePermission


class CanAddCardToGroup(BasePermission):
    """
    Permission class to check if a user can add a card to a group.
    """

    def has_permission(self, request, view):
        card_groups = request.data.get('card_groups')
        if not card_groups:
            return True
        user_groups = request.user.userprofile.card_groups.values_list('name', flat=True)
        for group_id in card_groups:
            if not user_groups.filter(pk=group_id).exists():
                return False
        return True


