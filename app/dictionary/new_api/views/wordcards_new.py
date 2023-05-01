from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dictionary.api.filters import WordCardFilter
from dictionary.api.paginations import StandardResultsSetPagination
from dictionary.api.permissions import CanAddCardToGroup
from dictionary.new_api.logical.views import mixins
from dictionary.new_api.serializers.worcards import WordCardSerializer, WordCardSerializerDetail, WordSerializerInternal
from dictionary.models import WordCard, CardGroup, Word, WordCardProgress
from dictionary.new_api.logical.views.service_based_apiview import ServiceListCreateAPIView, \
    ServiceRetrieveUpdateDestroyAPIView
from dictionary.services.wordcards import WordCardService
from langer import settings


class WordCardApiView(ServiceListCreateAPIView):
    permission_classes = (IsAuthenticated, CanAddCardToGroup)
    serializer_class = WordCardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WordCardFilter
    pagination_class = StandardResultsSetPagination
    service = WordCardService

    def get_queryset(self):
        return WordCard.objects.filter(owner=self.request.user.userprofile).order_by('id')

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context


class WordCardApiDetailView(ServiceRetrieveUpdateDestroyAPIView):
    serializer_class = WordCardSerializerDetail
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, CanAddCardToGroup)
    service_class = WordCardService

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardApiDetailViewGroup(WordCardApiDetailView, mixins.CreateModelMixin):
    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def get_queryset(self):
        return WordCard.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            # Создать копию карточки с новым владельцем
            # copy_data = request.data#serializer.validated_data.copy()
            self.create(request, *args, **kwargs)
            copy_serializer = self.get_serializer(data=request.data)
            # copy_serializer['owner'] = request.user
            copy_serializer.is_valid(raise_exception=True)
            copy_serializer.save()
            instance = copy_serializer.instance
            return Response(self.get_serializer(instance).data)
        else:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    def perform_destroy(self, instance: WordCard):
        instance.card_groups.remove(self.kwargs['group_pk'])
        instance.save()
        if not instance.card_groups.exists():
            print('удаляем карточку')
            if not settings.DEBUG:
                instance.delete()


class WordCardApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordCardSerializerDetail
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, CanAddCardToGroup)

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def get_queryset(self):
        return WordCard.objects.all()


class WordCardApiDetailViewGroup(WordCardApiDetailView):
    service_class = WordCardService

    class WordCardInGroupSerializer(serializers.ModelSerializer):
        word = WordSerializerInternal()
        translation = WordSerializerInternal()
        score = serializers.SerializerMethodField(read_only=True)

        card_groups = serializers.PrimaryKeyRelatedField(queryset=CardGroup.objects.all(), many=True, write_only=True)

        def validate(self, data):
            word_language = data['word']['language']

            card_group_language = CardGroup.objects.get(id=self.context['view'].kwargs['group_pk']).language_id
            if word_language.id != card_group_language:
                raise serializers.ValidationError("Язык слова должен совпадать с языком набора")
            return data

        def get_score(self, obj):
            try:
                return WordCardProgress.objects.get(card=obj.id, owner=self.context['userprofile']).score
            except WordCardProgress.DoesNotExist:
                return 0

        class Meta:
            model = WordCard
            exclude = ('owner', 'used_by', 'is_public',)

    serializer_class = WordCardInGroupSerializer

    def get_serializer_context(self, **kwargs):
        context = super(WordCardApiDetailView, self).get_serializer_context()
        context.update({"userprofile": self.request.user.userprofile})
        return context

    def get_queryset(self):
        return WordCard.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            # Создать копию карточки с новым владельцем
            # copy_data = request.data#serializer.validated_data.copy()

            copy_serializer = self.get_serializer(data=request.data)
            # copy_serializer['owner'] = request.user
            copy_serializer.is_valid(raise_exception=True)
            copy_serializer.save()
            instance = copy_serializer.instance
            return Response(self.get_serializer(instance).data)
        else:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    def perform_destroy(self, instance: WordCard):
        instance.card_groups.remove(self.kwargs['group_pk'])
        instance.save()
        if not instance.card_groups.exists():
            print('удаляем карточку')
            if not settings.DEBUG:
                instance.delete()
