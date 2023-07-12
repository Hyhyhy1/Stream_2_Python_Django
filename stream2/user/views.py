from django.shortcuts import get_object_or_404
from rest_framework import views, permissions, response
from .models import UserLikedSongs, UserBannedSongs, UserSubscriptions
from song.models import Song
from django.core.exceptions import ObjectDoesNotExist
from .serializer import UserLikedSongsSerializer, UserBannedSongsSerializer, UserSubscriptionsSerializer
from artist.models import Artist


class UserSongLikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        try:
            liked_song = UserLikedSongs.objects.get(song_id=song, user_id=request.user)
        except ObjectDoesNotExist:
            _ = UserLikedSongs.objects.create(user_id=request.user, song_id=song)
            return response.Response(data={"status": "liked"}, status=200)
        
        liked_song.delete()
        return response.Response(data={"status": "unliked"}, status=200)
    
class UserSongLikeListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        liked_songs = UserLikedSongs.objects.filter(user_id=request.user)
        serializer = UserLikedSongsSerializer(liked_songs, many=True)
        return response.Response(data=serializer.data)

        
        
class UserSongBannedView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        try:
            banned_song = UserBannedSongs.objects.get(song_id=song, user_id=request.user)
        except ObjectDoesNotExist:
            _ = UserBannedSongs.objects.create(user_id=request.user, song_id=song)
            return response.Response(data={"status": "banned"}, status=200)
        
        banned_song.delete()
        return response.Response(data={"status": "unbanned"}, status=200)
    
class UserSongBannedListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        banned_songs = UserBannedSongs.objects.filter(user_id=request.user)
        serializer = UserBannedSongsSerializer(banned_songs, many=True)
        return response.Response(data=serializer.data)


        
class UserSubscribeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, artist_id):
        artist = get_object_or_404(Artist, pk=artist_id)
        try:
            subscription = UserSubscriptions.objects.get(artist_id=artist, user_id=request.user)
        except ObjectDoesNotExist:
            _ = UserSubscriptions.objects.create(user_id=request.user, artist_id=artist)
            return response.Response(data={"status": "subscribed"}, status=200)
        
        subscription.delete()
        return response.Response(data={"status": "unsubscribed"}, status=200)
    
    
class UserSubscriptionsListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subscriptions = UserSubscriptions.objects.filter(user_id=request.user)
        serializer = UserSubscriptionsSerializer(subscriptions, many=True)
        return response.Response(data=serializer.data)