from dictionary.models import Word
from dictionary.new_api.logical.services.base_service import BaseService


class WordService(BaseService):
    model = Word
