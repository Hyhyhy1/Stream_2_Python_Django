from rest_framework import serializers
from .models import UserLikedSongs, UserBannedSongs, UserSubscriptions
from song.serializers import SongSerializer
from artist.serializers import ArtistSerializer

class UserLikedSongsSerializer(serializers.ModelSerializer):
    song_id = SongSerializer()
    class Meta:
        model = UserLikedSongs
        fields = "__all__"
    
class UserBannedSongsSerializer(serializers.ModelSerializer):
    song_id = SongSerializer()
    class Meta:
        model = UserBannedSongs
        fields = "__all__"

class UserSubscriptionsSerializer(serializers.ModelSerializer):
    artist_id = ArtistSerializer()
    class Meta:
        model = UserSubscriptions
        fields = "__all__"