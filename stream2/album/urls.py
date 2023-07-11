from django.urls import path
from . import views
from .views import AlbumAPI, AlbumList, AlbumCreator

urlpatterns = [
    path('api/v1/albumlist/<int:pk>', AlbumAPI.as_view()),
    path('api/v1/albumlist/', AlbumList.as_view()),
    path('api/v1/albumlist/create/', AlbumCreator.as_view()),
]
