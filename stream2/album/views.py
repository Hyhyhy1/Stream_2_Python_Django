import uuid

import boto3
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics, viewsets, parsers, status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from artist.models import Artist
from artist.views import ALLOWD_IMAGE_CONTENT_TYPES
from song.models import Song
from .models import Album
from .parser import MultipartJsonParser
from .serializes import AlbumSerializer, PostsSerializer


class AlbumList(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumCreator(generics.CreateAPIView):
    queryset = Album.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultipartJsonParser, JSONParser)
    serializer_class = AlbumSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if artist:= Artist.objects.get(user_id=request.user):
                pass
        except ObjectDoesNotExist:
            return Response(data= {'error': 'user is not artist'})

        image_url =""

        if request.data.get("media"):
            image_url = self.upload_image(request)
            print(f"{image_url=}")
            if not isinstance(image_url, str):
                return image_url

        artist = Album.objects.create(
            name = serializer.validated_data["name"],
            artist_id = artist,
            cover_uri = image_url,
        )
        # songs = Song.objects.all().filter(id=serializer.validated_data["songs"])
        # for song in songs:
        # artist.songs.set(Song.objects.all().filter(id=serializer.validated_data["songs"]).id)

        headers = self.get_success_headers(serializer.data)
        return Response(artist, status=status.HTTP_201_CREATED, headers=headers)

    def upload_image(self, request):
        file_obj = request.data.get("media")

        if file_obj.content_type not in ALLOWD_IMAGE_CONTENT_TYPES:
            return Response({"error": "bad content type"}, status=418)

        file_name = f'{uuid.uuid4()}.{file_obj.name.split(".")[-1]}'

        s3 = boto3.client('s3',
                          endpoint_url='https://s3.us-east-005.backblazeb2.com',
                          aws_access_key_id='0052f74eb7913790000000002',
                          aws_secret_access_key='K005UkQ2LN8YtYzMUdiBV2qNI/VO/ek')

        s3.upload_fileobj(file_obj.file, 'UrFUbe-videos', file_name)
        return 'https://UrFUbe-videos.s3.us-east-005.backblazeb2.com/' + file_name

class PostsViewset(viewsets.ModelViewSet):
    serializer_class = PostsSerializer
    queryset = Album.objects.all()



