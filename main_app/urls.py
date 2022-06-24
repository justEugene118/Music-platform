from django.urls import path, include
from main_app import views

app_name = 'main_app'


urlpatterns = [
    path('', views.main_view, name="music"),
    path('add_song/', views.add_song, name="add_song"),
    path('creator/', views.become_creator, name="become_creator"),
    path('<int:song_id>/', views.song_detail, name="song_detail"),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/<str:playlist_name>/', views.playlist_songs, name='playlist_songs'),
    path('favorite/', views.favorite, name='favourite'),
    path('recent/', views.recent, name='recent'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('play_recent_song/<int:song_id>/', views.play_recent_song, name='play_recent_song'),
    path('creator_page', views.creator_profile, name='creator_profile'),
    path('song/<int:song_id>/delete_song', views.song_delete, name='song_delete'),
]
