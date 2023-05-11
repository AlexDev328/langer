from dictionary.models import Language
from dictionary.api.logical.services.base_service import BaseService


class LanguageService(BaseService):
    model = Language
