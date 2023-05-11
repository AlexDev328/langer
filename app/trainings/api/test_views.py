from rest_framework import generics
from rest_framework.response import Response

from dictionary.models import Card
from trainings.api.test_serializer import CardTrainingSerializer


class CardsTrainingApiView(generics.RetrieveUpdateAPIView):
    serializer_class = CardTrainingSerializer

    def get(self, request, *args, **kwargs):
        print(request)
        word = Card.objects.get_random_words(user_id=request.user.id, language_id=2, count=1)[0]
        options = Card.objects.get_options_for_card(user_id=request.user.id, card=word, count=3)
        serializer = CardTrainingSerializer({'word': word.word.text, 'options': [*options, word.translation.text]})
        return Response(serializer.data)
