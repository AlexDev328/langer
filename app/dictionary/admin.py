from django.contrib import admin

from .models import Word, Card, CardProgress, Language, Deck

# Register your models here.


admin.site.register(Word)
admin.site.register(Card)
admin.site.register(Language)


class MembershipInline(admin.TabularInline):
    model = Deck.cards.through
    extra = 0

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public')

    inlines = [MembershipInline,]



admin.site.register(CardProgress)
