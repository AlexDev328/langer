from rest_framework import generics

from dictionary.api.logical.views.service_based_apiview import ServiceListCreateAPIView
from dictionary.api.serializers import LanguageSerializer
from dictionary.models import Language


class LanguageApiView(ServiceListCreateAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()



