from django.shortcuts import render
from uuid import uuid4
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Playlist
from .serializers import PlaylistSerializer
# Create your views here.


class PlaylistList(generics.ListAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class PlaylistAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class PlaylistCreator(generics.CreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer