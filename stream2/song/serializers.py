from rest_framework import serializers
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
