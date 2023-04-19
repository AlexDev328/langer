from django.urls import path

from alphabet.api.views import ListAlphabet, AlphabetDetail

urlpatterns = [
    path("alphabet", ListAlphabet.as_view(), name='alphabet list'),
    path("alphabet/<int:pk>", AlphabetDetail.as_view(), name='alphabet detail')
]
