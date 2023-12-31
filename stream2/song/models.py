from django.db import models
from artist.models import Artist
from user.models import User


class Song(models.Model):
    class Genre(models.TextChoices):
        ROCK = "Rock"
        RAP = "Rap"
        POP = "Pop"

    name = models.CharField(max_length=255, db_index=True)
    cover_url = models.CharField(max_length=512, null=True, blank=True)
    song_uri = models.CharField(max_length=512)
    lyrics = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=2, choices=[
        ("RU", "Russian"),
        ("EN", "English"),
        ("ES", "Spanish")
    ])
    instrumental = models.BooleanField()
    explicit = models.BooleanField()
    genre = models.CharField(max_length=64, choices=Genre.choices)
    artists = models.ManyToManyField(
        Artist
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    

class SongComments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"comment from {self.user_id}"