from django.urls import path
from song.views import SongList, SongAPI, SongCreator


urlpatterns = [
    path('api/song/', SongList.as_view()),
    path('api/song/<int:pk>/', SongAPI.as_view()),
    path('api/song/create/', SongCreator.as_view()),
]