from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dictionary.models import Language, Card, Word, Deck
from userprofile.models import UserProfile


class CardTests(APITestCase):
    data = {}

    @classmethod
    def setUpTestData(cls):
        cls.lang_1 = Language.objects.create(name='Английский')
        cls.lang_2 = Language.objects.create(name='Русский')
        cls.user = User.objects.create(username='test', password='test')
        cls.userprofile = UserProfile.objects.create(default_language=cls.lang_1, user=cls.user)

    def create_own_deck(self, name, language, owner) -> Deck:
        return Deck.objects.create(name=name, language=language, owner=owner)

    def create_second_user_pack(self):
        second_user = User.objects.create(username='test2', password='test')
        second_userprofile = UserProfile.objects.create(default_language=self.lang_1, user=second_user)
        return second_user, second_userprofile

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_test(self):
        assert True == True

    def test_create_card_with_deck(self):
        """
        Ensure we can create a new card object with one deck.
        """

        url = reverse("cards")
        deck_1 = self.create_own_deck('группа 1', self.lang_1, owner=self.userprofile)
        data = {
            "word": {
                "text": "test",
                "language": self.lang_1.id
            },
            "translation": {
                "text": "тест",
                "language": self.lang_2.id
            },
            "decks": [deck_1.id],
            "transcription": "",
            "description": "",
            "example": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.get().example, '')
        self.assertEqual(list(Card.objects.get().decks.all().values_list('id', flat=True)), [deck_1.id])

    def test_create_card_with_2_deck(self):
        """
        Ensure we can create a new card object with two decks.
        """

        url = reverse("cards")
        deck_1 = self.create_own_deck('группа 1', self.lang_1, owner=self.userprofile)
        deck_2 = self.create_own_deck('группа 2', self.lang_1, owner=self.userprofile)
        data = {
            "word": {
                "text": "test",
                "language": self.lang_1.id
            },
            "translation": {
                "text": "тест",
                "language": self.lang_2.id
            },
            "decks": [deck_1.id, deck_2.id],
            "transcription": "",
            "description": "",
            "example": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.get().example, '')
        self.assertEqual(list(Card.objects.get().decks.all().values_list('id', flat=True)), [deck_1.id, deck_2.id])

    def test_create_card_without_decks(self):
        """
        Ensure we can create a new card object without any deck.
        """
        url = reverse("cards")
        data = {
            "word": {
                "text": "test",
                "language": self.lang_1.id
            },
            "translation": {
                "text": "тест",
                "language": self.lang_2.id
            },
            "decks": [],
            "transcription": "",
            "description": "",
            "example": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.get().example, '')


    def test_create_card_with_another_user_decks(self):
        """
        Ensure we can't create a new card object with another user's deck.
        """
        another_user, another_userprofile = self.create_second_user_pack()
        deck_1 = self.create_own_deck('группа другого пользователя', self.lang_1, owner=another_userprofile)

        url = reverse("cards")
        data = {
            "word": {
                "text": "test",
                "language": self.lang_1.id
            },
            "translation": {
                "text": "тест",
                "language": self.lang_2.id
            },
            "decks": [deck_1.id],
            "transcription": "",
            "description": "",
            "example": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_card_with_another_user_decks(self):
        """
        Ensure we can't create a new card object with another user's deck.
        """
        another_user, another_userprofile = self.create_second_user_pack()
        deck_1 = self.create_own_deck('группа другого пользователя', self.lang_1, owner=another_userprofile)
        deck_2 = self.create_own_deck('группа 1', self.lang_1, owner=self.userprofile)
        url = reverse("cards")
        data = {
            "word": {
                "text": "test",
                "language": self.lang_1.id
            },
            "translation": {
                "text": "тест",
                "language": self.lang_2.id
            },
            "decks": [deck_1.id, deck_2.id],
            "transcription": "",
            "description": "",
            "example": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # СОЗДАНИЕ
    # создать карту без колод
    # создать карту с 1 колодой (своей)*
    # создать карту с 2 колодами (своими)*
    # создать карту с 1 колодой (чужой)*
    # создать карту с 2 колодами (1 своя, 1 чужая)*

    # РЕДАКТИРОВАНИЕ
    # изменить свою карту (все нессылочные поля)
    # изменить/удалить чужую карту по основному урлу нельзя
    # изменить чужую карту (нет подписки ни на карту ни на группу)
    # изменить чужую карту (есть подписка на колоду)
    # изменить чужую карту (есть подписка на карту)
    # свою карту без колод добавить в свою колоду
    # свою карту без колод добавить в 2 своих колоды
    # свою карту без колод добавить в чужую колоду
    # свою карту без колод добавить в 2 колоды: одна своя, одна чужая
    # свою карту в своей колоде убрать из колоды
    # свою карту в 2 колодах убрать из обеих колод
    # свою карту в 2 колодах убрать из одной колоды
    # свою карту, добавленную в свою колоду и в чужую колоду, удалить из своей
    # свою карту, добавленную в свою колоду и в чужую колоду, удалить из чужой
    # свою карту, добавленную в свою колоду и в чужую колоду, удалить из обеих
    # удалить свою карту без колод
    # удалить свою карту, добавленную в свою колоду
    # удалить свою карту, добавленную в чужую колоду
    # удалить свою карту, добавленную в 2 колоды: одну свою и одну чужую

    # ДОСТУП
    # сделать свою непубличную карту без колод публичной
    # сделать свою публичную карту без колод непубличной
    # сделать свою публичную карту, добавленную в чужую колоду, непубличной
    # своя непубличная карта, находится в своей колоде, на которую кто-то подписан, и мы делаем эту карту публичной
    # своя публичная карту, находится в своей колоде, на которую кто-то подписан, и мы делаем эту карту непубличной


