from django.urls import path
from playlist.views import PlaylistList, PlaylistAPI, PlaylistCreator


urlpatterns = [
    path('api/playlist/', PlaylistList.as_view()),
    path('api/playlist/<int:pk>/', PlaylistAPI.as_view()),
    path('api/playlist/create/', PlaylistCreator.as_view()),

]