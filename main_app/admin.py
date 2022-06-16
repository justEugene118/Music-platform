from django.contrib import admin
from .models import Song, Playlist, Favorite, Recent, Comment

# Register your models here.
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Favorite)
admin.site.register(Recent)
admin.site.register(Comment)
