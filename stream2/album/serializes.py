from rest_framework import serializers
from .models import Album

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["name", "songs" , "cover_uri", "created_at", "updated_at"]

class PostsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"
