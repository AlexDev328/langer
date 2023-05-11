from rest_framework import generics

from dictionary.api.logical.views.service_based_apiview import ServiceListCreateApiView
from dictionary.api.serializers import LanguageSerializer
from dictionary.models import Language


class LanguageApiView(ServiceListCreateApiView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()



