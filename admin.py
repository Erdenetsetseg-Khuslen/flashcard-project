from django.contrib import admin
from .models import Kanji, UserKanji

admin.site.register(Kanji)
admin.site.register(UserKanji)
