from rest_framework import generics, status
from rest_framework.response import Response
from trainings.api.test_serializer import WordCardsTrainingSerializer
from dictionary.models import WordCard, WordCardProgress


class TrainingCheckApiView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        print(request)
        try:
            progress, _ = WordCardProgress.objects.get_or_create(user=self.request.user.userprofile,
                                                                 card_id=kwargs['pk'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.data['answer'] == WordCard.objects.get(id=kwargs['pk']).translation.text:
            progress.score += 1
            progress.save()
            return Response(status=status.HTTP_200_OK,
                            data={'right_answer': WordCard.objects.get(id=kwargs['pk']).translation.text,
                                  'correct': True})
        return Response(status=status.HTTP_200_OK,
                        data={'right_answer': WordCard.objects.get(id=kwargs['pk']).translation.text, 'correct': False})


class WordCardsTrainingApiView(generics.RetrieveUpdateAPIView):
    serializer_class = WordCardsTrainingSerializer

    def get(self, request, *args, **kwargs):
        print(request)
        word = WordCard.objects.get_random_words(user_id=request.user.id, language_id=2, count=1)[0]
        options = WordCard.objects.get_options_for_wordcard(user_id=request.user.id, wordcard=word,
                                                            count=3)
        serializer = WordCardsTrainingSerializer({'wordcard': word, 'options': list(options)})
        return Response(serializer.data)
