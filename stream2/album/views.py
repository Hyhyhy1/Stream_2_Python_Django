from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Album
from .serializes import AlbumSerializer


# class AlbumAPIView(APIView):
#     def get(self):
#         return Response({'title': 'Hi'})

class AlbumList(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumCreator(generics.CreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer



