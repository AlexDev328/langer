from django.contrib import admin
from .models import Word, WordCard, WordCardProgress, Language, CardGroup

# Register your models here.


admin.site.register(Word)
admin.site.register(WordCard)
admin.site.register(Language)


@admin.register(CardGroup)
class CardGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_public')


admin.site.register(WordCardProgress)
