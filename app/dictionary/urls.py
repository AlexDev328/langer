from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
#now import the views.py file into this code
from .views import create_new_wordcard, index, mycards




urlpatterns=[
  path("login/", LoginView.as_view(), name="login"),
  path("logout/", LogoutView.as_view(), name="logout"),
  path('',index),
  path('add_new_card', create_new_wordcard),
  path('mycards', mycards),
]