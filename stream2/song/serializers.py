from rest_framework import serializers
from .models import Song
from artist.models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"


class SongDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["name", "cover_url", "lyrics", "language", "instrumental", "explicit", "genre"]


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
