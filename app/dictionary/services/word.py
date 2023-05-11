from dictionary.models import Word
from dictionary.api.logical.services.base_service import BaseService


class WordService(BaseService):
    model = Word

    def get_or_create(self, **kwargs):
        return self.model.objects.get_or_create(**dict(self.data))
