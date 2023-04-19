from django.contrib import admin

from alphabet.models import Letter, LetterGroup, Alphabet, AlphabetEntry

# Register your models here.


admin.site.register(Letter)

admin.site.register(LetterGroup)

admin.site.register(Alphabet)
admin.site.register(AlphabetEntry)
