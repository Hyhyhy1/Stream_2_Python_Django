from django.db import models
from artist.models import Artist
from song.models import Song

class Album(models.Model):
    name = models.CharField(max_length=255)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)

    songs = models.ManyToManyField(Song)
    cover_uri = models.CharField(max_length=512)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name