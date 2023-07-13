from rest_framework import viewsets, permissions, status, exceptions
import boto3
from rest_framework.response import Response
from .models import Artist, ArtistSocialLinks
from .serializers import ArtistSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from .parser import MultipartJsonParser
import uuid


ALLOWD_IMAGE_CONTENT_TYPES = ["image/png", "image/jpeg"]

class UserIsAlreadyArtistException(exceptions.APIException):
    status_code = 400
    default_detail = "User is already artist"

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultipartJsonParser, JSONParser)

    def check_object_permission(self, request, obj):
        print(request.user, obj.user_id)
        if request.user.id != obj.user_id.id and not request.user.is_staff:
            raise exceptions.PermissionDenied
            

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            if Artist.objects.get(user_id=request.user):
                raise UserIsAlreadyArtistException
        except ObjectDoesNotExist:
            pass
        
        if request.data.get("media"):
            image_url = self.upload_image(request)
            print(f"{image_url=}")
            if not isinstance(image_url, str):
                return image_url
            
            
        artist = Artist.objects.create(
            **serializer.validated_data,
            user_id=request.user,
            picture_url=image_url,
        )
        
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
    
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.check_object_permission(request, instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permission(request, instance)
        instance.delete()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)