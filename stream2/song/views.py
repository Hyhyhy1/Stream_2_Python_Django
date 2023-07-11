from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Song
from .serializers import SongSerializer
# Create your views here.


class SongList(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongCreator(generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer




