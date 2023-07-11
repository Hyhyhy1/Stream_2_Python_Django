from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Playlist
# Create your views here.
class playlistApiView(APIView):
    def get(self, request):
        lst = Playlist.objects.all().values()
        return Response({'data': list(lst)})