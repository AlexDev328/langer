from rest_framework import generics, status
from rest_framework.response import Response
from trainings.api.serializers import WordCardTrainingSerializer
from dictionary.models import WordCard, WordCardProgress
from trainings.models import WordCardTraining


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
    serializer_class = WordCardTrainingSerializer

    def get(self, request, *args, **kwargs):
        print(request)
        wordcard = WordCard.objects.get_random_words(user_id=request.user.id, language_id=2, count=1)[0]
        options = WordCard.objects.get_options_for_wordcard(user_id=request.user.id, wordcard=wordcard,
                                                            count=3)
        WordCardTraining.objects.filter(user=self.request.user.userprofile).delete()
        trainings = WordCardTraining.objects.create(wordcard=wordcard, answer=wordcard.translation.text,
                                                    user=self.request.user.userprofile)
        serializer = WordCardTrainingSerializer(
            {'id': trainings.id, 'question': wordcard.word.text, 'options': [*options, wordcard.translation.text]})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            training = WordCardTraining.objects.get(id=kwargs['pk'])
            progress, _ = WordCardProgress.objects.get_or_create(user=self.request.user.userprofile,
                                                                 card=training.wordcard)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.data['answer'] == training.answer:
            progress.score += 1
            progress.save()
            return Response(status=status.HTTP_200_OK,
                            data={'right_answer': training.answer,
                                  'correct': True})
        return Response(status=status.HTTP_200_OK,
                        data={'right_answer': training.answer, 'correct': False})
