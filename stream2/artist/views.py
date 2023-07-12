from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.response import Response
from .models import Artist, ArtistSocialLinks
from .serializers import ArtistSerializer
from django.core.exceptions import ObjectDoesNotExist


class UserIsAlreadyArtistException(exceptions.APIException):
    status_code = 400
    default_detail = "User is already artist"

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
            
        artist = Artist.objects.create(
            user_id=request.user,
            **serializer.validated_data
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(artist, status=status.HTTP_201_CREATED, headers=headers)
    
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