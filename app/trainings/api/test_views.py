from rest_framework import generics
from rest_framework.response import Response

from dictionary.models import WordCard
from trainings.api.test_serializer import WordCardTrainingSerializer


class WordCardsTrainingApiView(generics.RetrieveUpdateAPIView):
    serializer_class = WordCardTrainingSerializer

    def get(self, request, *args, **kwargs):
        print(request)
        word = WordCard.objects.get_random_words(user_id=request.user.id, language_id=2, count=1)[0]
        options = WordCard.objects.get_options_for_wordcard(user_id=request.user.id, wordcard=word,
                                                            count=3)
        serializer = WordCardTrainingSerializer({'word': word.word.text, 'options': [*options, word.translation.text]})
        return Response(serializer.data)
