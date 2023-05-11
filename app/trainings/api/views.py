from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from trainings.api.serializers import CardTrainingSerializer
from dictionary.models import Card, CardProgress
from trainings.models import CardTraining


class TrainingCheckApiView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        print(request)
        try:
            progress, _ = CardProgress.objects.get_or_create(user=self.request.user.userprofile,
                                                             card_id=kwargs['pk'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.data['answer'] == Card.objects.get(id=kwargs['pk']).translation.text:
            progress.score += 1
            progress.save()
            return Response(status=status.HTTP_200_OK,
                            data={'right_answer': Card.objects.get(id=kwargs['pk']).translation.text,
                                  'correct': True})
        return Response(status=status.HTTP_200_OK,
                        data={'right_answer': Card.objects.get(id=kwargs['pk']).translation.text, 'correct': False})


class TrainingResultsSerializer(serializers.Serializer):
    answer = serializers.CharField()
    correct = serializers.BooleanField()


class CardsTrainingApiView(APIView):
    #CardTrainingSerializer
    def get(self, request, *args, **kwargs):
        print(request)
        card = Card.training.get_card_for_training(language_id=2, user=request.user.userprofile)
        options = Card.training.get_options_set(card, request.user.userprofile)
        #training_data = Card.training.get_training_set(language_id=2, user=request.user, count=5)

        # card = Card.objects.get_random_words(user_id=request.user.id, language_id=2, count=1)[0]
        # options = Card.objects.get_options_for_card(user_id=request.user.id, card=card,
        #                                                   count=3)
        CardTraining.objects.filter(user=self.request.user.userprofile).delete()
        training = CardTraining.objects.create(card=card, answer=card.translation.text,
                                               user=self.request.user.userprofile)
        serializer = CardTrainingSerializer(
            {'id': training.id, 'question': card.word.text,
             'options': [*options, card.translation.text]})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            training = CardTraining.objects.get(id=kwargs['pk'])
            progress, _ = CardProgress.objects.get_or_create(owner=self.request.user.userprofile,
                                                             card=training.card)
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
