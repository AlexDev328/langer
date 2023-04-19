from rest_framework import generics, serializers

from rest_framework.mixins import ListModelMixin

from alphabet.models import Alphabet, Letter, AlphabetEntry


class ListAlphabet(generics.ListAPIView):
    queryset = Alphabet.objects.all()
    filterset_fields = ['language']

    class AlphabetSerializer(serializers.ModelSerializer):
        class Meta:
            model = Alphabet
            fields = '__all__'

    serializer_class = AlphabetSerializer


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        exclude = ("language",)


class AlphabetEntrySerializer(serializers.ModelSerializer):
    letter = LetterSerializer()

    class Meta:
        model = AlphabetEntry
        exclude = ("alphabet",)


class AlphabetDetail(generics.RetrieveAPIView):
    queryset = Alphabet.objects.all()

    class AlphabetDetailSerializer(serializers.ModelSerializer):
        alphabetentry_set = AlphabetEntrySerializer(many=True)

        class Meta:
            model = Alphabet
            fields = "__all__"

    serializer_class = AlphabetDetailSerializer
