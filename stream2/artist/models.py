from django.db import models
from user.models import User

class Artist(models.Model):
    class Sex(models.IntegerChoices):
        MALE = 1
        FEMALE = 2
        OTHER = 3
    
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    picture_url = models.CharField(max_length=512, blank=True, null=True)
    about = models.TextField(max_length=512, blank=True, null=True)
    sex = models.IntegerField(choices=Sex.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return self.name
    