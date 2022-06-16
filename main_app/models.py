from django.db import models
from users_app.models import CustomUser
from datetime import datetime

# Create your models here.


class Song(models.Model):
    song_name = models.TextField()
    creator = models.TextField()
    audio_file = models.FileField(blank=True, null=True)
    audio_link = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=20)
    genres = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class Playlist(models.Model):
    playlist_name = models.CharField(max_length=100)
    creator_id = models.IntegerField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now())


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Recent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now())
    rating = models.IntegerField(default=0)
