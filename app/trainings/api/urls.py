from django.urls import path

from .views import CardsTrainingApiView, TrainingCheckApiView

urlpatterns = [
    path("trainings/simple", CardsTrainingApiView.as_view(), name='simple training'),
    path("trainings/test", CardsTrainingApiView.as_view(), name='test training'),
    path("trainings/test/<str:pk>", CardsTrainingApiView.as_view(), name='test'),
    path("trainings/simple/correct/<int:pk>", TrainingCheckApiView.as_view(), name='training_results'),
]
