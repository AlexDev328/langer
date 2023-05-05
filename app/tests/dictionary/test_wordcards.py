from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dictionary.models import Language, WordCard, Word, CardGroup
from userprofile.models import UserProfile


class WordCardTests(APITestCase):
    data = {}

    def setUp(self) -> None:
        print(f'setup {self.__class__.__name__}')
        self.lang_1 = Language.objects.create(name='Английский')
        self.lang_2 = Language.objects.create(name='Русский')
        self.user = User.objects.create(username='test', password='test')
        self.userprofile = UserProfile.objects.create(default_language=self.lang_1, user=self.user)
        self.client.force_login(self.user)

    def test_test(self):
        assert True == True

    def test_create_wordcard(self):
        """
        Ensure we can create a new wordcard object.
        """
        url = reverse("wordcards listcreate")
        data = {
            "word": {
                "text": "test",
                "language": self.lang_1.id
            },
            "translation": {
                "text": "тест",
                "language": self.lang_2.id
            },
            "card_groups": [],
            "transcription": "",
            "description": "",
            "example": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WordCard.objects.count(), 1)
        self.assertEqual(WordCard.objects.get().example, '')

    def test_create_wordcard_without_cardgroups(self):
        """
        Ensure we can create a new wordcard object.
        """
        url = reverse("wordcards listcreate")
        data = {
            "word": {
                "text": "test",
                "language": self.lang_1.id
            },
            "translation": {
                "text": "тест",
                "language": self.lang_2.id
            },
            "card_groups": [],
            "transcription": "",
            "description": "",
            "example": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WordCard.objects.count(), 1)
        self.assertEqual(WordCard.objects.get().example, '')


class WordCardGroupTests(WordCardTests):
    data = {}
