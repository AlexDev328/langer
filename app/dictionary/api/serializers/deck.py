from rest_framework import serializers

from dictionary.models import Deck, Card, Language


class DeckSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField(read_only=True)
    card_learned = serializers.SerializerMethodField()
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())

    class Meta:
        model = Deck
        exclude = ('owner', 'used_by', 'is_public')

    def get_card_learned(self, obj: Deck) -> int:
        return obj.cards.filter(cardprogress__owner=self.context['request'].user.userprofile,
                                cardprogress__score=10).count()


class DeckExpandSerializer(serializers.ModelSerializer):
    cards = serializers.PrimaryKeyRelatedField(many=True, queryset=Card.objects.all())

    class Meta:
        model = Deck
        fields = ('cards',)


