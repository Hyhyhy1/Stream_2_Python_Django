from django.urls import path
from song.views import SongList, SongAPI, AudioUploadView


urlpatterns = [
    path('api/song/', SongList.as_view()),
    path('api/song/<int:pk>/', SongAPI.as_view()),
    path('api/song/upload/', AudioUploadView.as_view(), name='file-upload'),

]