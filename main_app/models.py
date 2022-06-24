from django.db import models
from users_app.models import CustomUser
from datetime import datetime

from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Song(models.Model):
    GENRE_CHOICES = (
        ('ROCK', 'Rock'),
        ('METAL', 'Metal'),
        ('POP', 'Pop'),
        ('HIP-HOP', 'Hip-Hop'),
        ('INDY', 'Indy'),
        ('COUNTRY', 'Country'),
        ('BLUES', 'Blues'),
        ('CLASSIC', 'Classic')
    )

    song_name = models.CharField(max_length=50, unique=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    audio_file = models.FileField(blank=True, upload_to='Songs/', null=True)
    image_file = models.ImageField(blank=True, upload_to='Song_Image/', null=True, default='Song_Image/default.jpg')
    genres = MultiSelectField(choices=GENRE_CHOICES)
    date_added = models.DateTimeField(default=datetime.now())
    data_created = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.song_name


class Playlist(models.Model):
    playlist_name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
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
    rating = models.IntegerField(default=None, blank=True, null=True, validators=[MaxValueValidator(10), MinValueValidator(1)])
