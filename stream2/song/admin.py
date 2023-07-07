from django.contrib import admin
from .models import Song, SongComments


admin.site.register(Song)
admin.site.register(SongComments)

