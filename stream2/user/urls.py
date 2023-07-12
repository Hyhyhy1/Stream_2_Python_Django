from django.urls import path
from .views import UserSongLikeView, UserSongLikeListView, UserSongBannedListView, UserSongBannedView, UserSubscribeView, UserSubscriptionsListView



urlpatterns = [
    path('api/song/<int:song_id>/like/', UserSongLikeView.as_view()),
    path('api/users/likes/', UserSongLikeListView.as_view()),

    path('api/song/<int:song_id>/ban/', UserSongBannedView.as_view()),
    path('api/users/bans/', UserSongBannedListView.as_view()),

    path('api/artist/<int:artist_id>/subscribe/', UserSubscribeView.as_view()),
    path('api/users/subscriptions/', UserSubscriptionsListView.as_view()),
]