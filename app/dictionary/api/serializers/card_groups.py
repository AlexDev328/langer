from rest_framework import serializers

from dictionary.models import CardGroup, WordCard


class CardGroupSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField(read_only=True)
    card_learned = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CardGroup
        exclude = ('owner', 'used_by', 'is_public')

    def get_card_learned(self, obj: CardGroup):
        return obj.wordcards.filter(wordcardprogress__owner=self.context['request'].user.userprofile,
                                    wordcardprogress__score=10).count()


class CardGroupExpandSerializer(serializers.ModelSerializer):
    wordcards = serializers.PrimaryKeyRelatedField(many=True, queryset=WordCard.objects.all())

    class Meta:
        model = CardGroup
        fields = ('wordcards',)

    def update(self, instance, validated_data):
        new = set([i.id for i in validated_data['wordcards']])
        old = set(instance.wordcards.all().values_list('id', flat=True))
        instance.wordcards.set(old | new)
        return instance
