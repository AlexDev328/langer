from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from dictionary.new_api.serializers import CardGroupSerializer, WordSerializerInternal, CardGroupExpandSerializer
from dictionary.models import CardGroup, WordCard, WordCardProgress
from rest_framework import serializers
from dictionary.new_api.logical.views.service_based_apiview import ServiceListCreateAPIView, \
    ServiceRetrieveUpdateDestroyAPIView, ServiceUpdateAPIView
from dictionary.new_api.paginations import StandardResultsSetPagination
from dictionary.new_api.permissions import CanAddCardToGroup
from dictionary.services.cardgroups import CardGroupService, CardGroupExpandingService
from dictionary.services.wordcards import WordCardService


class CardGroupsListAPI(ServiceListCreateAPIView):
    serializer_class = CardGroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['language']
    pagination_class = StandardResultsSetPagination
    service_class = CardGroupService

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def perform_create(self, service):
        return service.save(owner=self.request.user.userprofile)


class CardGroupsCollectionAPI(ServiceListCreateAPIView):
    permission_classes = [IsAuthenticated, CanAddCardToGroup]
    pagination_class = StandardResultsSetPagination
    service_class = WordCardService

    class WordCardSerializer(serializers.ModelSerializer):
        word = WordSerializerInternal()
        translation = WordSerializerInternal()
        score = serializers.SerializerMethodField()

        def validate(self, data):
            word_language = data['word']['language']

            card_group_language = CardGroup.objects.get(id=self.context['view'].kwargs['pk']).language
            if word_language != card_group_language:
                raise serializers.ValidationError("Язык слова должен совпадать с языком набора")
            return data

        def get_score(self, obj):
            try:
                return WordCardProgress.objects.get(card=obj.id, owner=self.context['userprofile']).score
            except WordCardProgress.DoesNotExist:
                return 0

        class Meta:
            model = WordCard
            exclude = ('owner', 'used_by', 'is_public', 'card_groups')

    serializer_class = WordCardSerializer

    def get_queryset(self):
        return WordCard.objects.filter(card_groups=self.kwargs['pk'])

    def get_serializer_context(self, **kwargs):
        context = super(CardGroupsCollectionAPI, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context


class CardGroupsCollectionAPIPageable(CardGroupsCollectionAPI):
    permission_classes = [IsAuthenticated, CanAddCardToGroup]
    pagination_class = StandardResultsSetPagination


class CardGroupsExtendAPI(ServiceUpdateAPIView):
    serializer_class = CardGroupExpandSerializer
    service_class = CardGroupExpandingService

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile)


class CardGroupsDetailAPI(ServiceRetrieveUpdateDestroyAPIView):
    serializer_class = CardGroupSerializer

    def get_queryset(self):
        return CardGroup.objects.filter(owner=self.request.user.userprofile)
