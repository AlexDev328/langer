from rest_framework import serializers

from dictionary.models import CardGroup, WordCard, Language


class CardGroupSerializer(serializers.ModelSerializer):
    card_count = serializers.IntegerField(read_only=True)
    card_learned = serializers.SerializerMethodField()
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())

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


