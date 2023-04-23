from django_filters.rest_framework import DjangoFilterBackend

from dictionary.api.serializers import CardGroupSerializer
from dictionary.models import CardGroup
from dictionary.new_api.logical.views.service_based_apiview import ServiceListCreateAPIView
from dictionary.new_api.paginations import StandardResultsSetPagination


class CardGroupsListAPI(ServiceListCreateAPIView):
    serializer_class = CardGroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def perform_create(self, serializer):
        CardGroup.objects.create(*serializer.data, owner=self.request.user.userprofile)
        # serializer.save(owner=self.request.user.userprofile)
