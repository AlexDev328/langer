from django.contrib.auth.models import User

from dictionary.models import WordCard


def process_update_wordcard(instance:WordCard, user:User, update_data:dict):
    if update_data.get('card_groups'):
        #check ownership on card_groups

