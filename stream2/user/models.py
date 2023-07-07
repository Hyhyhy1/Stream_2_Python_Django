from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    ordering = ('email',)
    
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )    
    first_name = models.CharField(_("first name"), max_length=150) # Make first and last names required
    last_name = models.CharField(_("last name"), max_length=150)

    objects = CustomUserManager()
    def __str__(self) -> str:
        return self.email
 
    

class UserSubscriptions(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    artist_id = models.ForeignKey("artist.Artist", on_delete=models.CASCADE)

class UserLikedSongs(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.ForeignKey("song.Song", on_delete=models.CASCADE)

class UserBannedSongs(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.ForeignKey("song.Song", on_delete=models.CASCADE)