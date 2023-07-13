from django.forms import model_to_dict

import boto3
from uuid import uuid4
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser


from .models import Song
from .serializers import SongSerializer, FileUploadSerializer, SongDataSerializer
# Create your views here.


class SongList(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class AudioUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    #queryset = Song.objects.all()
    #serializer_class = SongSerializer
    def post(self, request, *args, **kwargs):

        serializer = SongDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_url = self.UploadFile(request)
        serializer.validated_data['song_uri'] = file_url
        #serializer.validated_data['artists'] = request.user.id
        serializer = SongSerializer(data=serializer.validated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def UploadFile(self, request, allowed_content_type: list[str] = None):
        if allowed_content_type is None:
            allowed_content_type = ["audio/mpeg", "audio/x-flac"]

        serializer = FileUploadSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=400)

        file_obj = serializer.validated_data['file']
        if file_obj.content_type not in allowed_content_type:
            return Response(serializer.errors, status=418)  #TODO добавить описание про некорректный формат, но я не знаю как

        file_name = f'{uuid4()}.{file_obj.name.split(".")[-1]}'  #вставить для создания каталогов пользователей{user_id}/

        # подключалось тестовое облако, заменить все данные на нужные
        s3 = boto3.client('s3',
                          endpoint_url='https://s3.us-east-005.backblazeb2.com',
                          aws_access_key_id='0052f74eb7913790000000002',
                          aws_secret_access_key='K005UkQ2LN8YtYzMUdiBV2qNI/VO/ek')

        s3.upload_fileobj(file_obj, 'UrFUbe-videos', file_name)
        return 'https://UrFUbe-videos.s3.us-east-005.backblazeb2.com/' + file_name

