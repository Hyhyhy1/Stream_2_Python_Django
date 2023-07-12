from django.forms import model_to_dict

import boto3
from uuid import uuid4
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser


from .models import Song
from .serializers import SongSerializer, FileUploadSerializer
# Create your views here.


class SongList(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class AudioUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        file_obj = request.FILES['file']
        print(request)
        print(file_obj)
        print(request.data)

        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']
            if file_obj.content_type != 'audio/mpeg' and file_obj.content_type != 'audio/x-flac':
                return Response(serializer.errors, status=418) #для будущих поколений - добавьте описание про некорректный формат

            file_name = f'{uuid4()}.{file_obj.name.split(".")[-1]}' #если будет получен uuid юзера можно добавить создание папок. Добавить в начало {user.id}/

            #подключалось тестовое облако, заменить все данные на нужные
            s3 = boto3.client('s3',
                    endpoint_url='https://s3.us-east-005.backblazeb2.com',
                    aws_access_key_id='',
                    aws_secret_access_key='')

            s3.upload_fileobj(file_obj, 'UrFUbe-videos', file_name)
            return Response({'url': 'https://UrFUbe-videos.s3.us-east-005.backblazeb2.com/' + file_name})
        else:
            return Response(serializer.errors, status=400)


