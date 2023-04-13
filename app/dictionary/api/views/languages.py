from rest_framework import generics

from dictionary.api.serializers import LanguageSerializer
from dictionary.models import Language


class LanguageApiView(generics.ListCreateAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()



