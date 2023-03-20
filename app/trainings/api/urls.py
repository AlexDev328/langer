from django.urls import path

from .views import WordCardsTrainingApiView, TrainingCheckApiView

urlpatterns = [
    path("trainings/simple", WordCardsTrainingApiView.as_view(), name='simple training'),
    path("trainings/simple/correct/<int:pk>", TrainingCheckApiView.as_view(), name='training_results'),
]
