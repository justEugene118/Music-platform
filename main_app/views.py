from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .forms import *
from .models import *
from users_app.models import CustomUser
from django.contrib import messages
from django.db.models import Q, Avg


# Create your views here.

def main_view(request):
    template_name = 'main_app/main.html'
    context = {}

    if request.user.is_authenticated:

        # last played song for player
        first_time = False
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            first_time = True
            last_played_song = Song.objects.get(id=1)

        # playlist
        playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct

        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if recent and request.user.is_authenticated:
            recent_id = [each['song_id'] for each in recent]
            recent_songs_unsorted = Song.objects.filter(id__in=recent_id, recent__user=request.user)
            recent_songs = list()
            for id in recent_id:
                recent_songs.append(recent_songs_unsorted.get(id=id))
        else:
            recent_songs = None

        if len(request.GET) > 0:
            search_query = request.GET.get('q')
            filtered_songs = Song.objects.filter(Q(song_name__icontains=search_query)).distinct()
            context = {
                'first_time': first_time,
                'last_played': last_played_song,
                'playlists': playlists,
                'recent_songs': filtered_songs,
                'query_search': True}
            return render(request, template_name, context)

        context = {
            'first_time': first_time,
            'last_played': last_played_song,
            'playlists': playlists,
            'recent_songs': recent_songs,
            'query_search': False
        }

        return render(request, template_name, context)
    else:
        return redirect('entry_app:main')


def song_detail(request, song_id):
    context = {}

    if request.user.is_authenticated:
        songs = Song.objects.filter(id=song_id).first()

        # add data to recent
        if list(Recent.objects.filter(song=songs, user=request.user).values()):
            data = Recent.objects.filter(song=songs, user=request.user)
            data.delete()
        data = Recent(song=songs, user=request.user)
        data.save()

        # Last played song
        last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            last_played_song = Song.objects.get(id=1)

        playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
        is_favourite = Favorite.objects.filter(user=request.user).filter(song=song_id).values('is_fav')
        comments = Comment.objects.filter(song=Song.objects.get(id=song_id)).distinct

        if request.method == "POST":
            if 'playlist' in request.POST:
                playlist_name = request.POST["playlist"]
                q = Playlist(user=request.user, song=songs, playlist_name=playlist_name)
                q.save()
                messages.success(request, "Song added to playlist!")
            elif 'add-fav' in request.POST:
                is_fav = True
                query = Favorite(user=request.user, song=songs, is_fav=is_fav)
                print(f'query: {query}')
                query.save()
                messages.success(request, "Added to favorite!")
                return redirect('entry_app:main_app:song_detail', song_id=song_id)
            elif 'rm-fav' in request.POST:
                is_fav = True
                query = Favorite.objects.filter(user=request.user, song=songs, is_fav=is_fav)
                print(f'user: {request.user}')
                print(f'song: {songs.id} - {songs}')
                print(f'query: {query}')
                query.delete()
                messages.success(request, "Removed from favorite!")
                return redirect('entry_app:main_app:song_detail', song_id=song_id)

        if request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                form.user = request.user
                form.song = Song.objects.get(id=song_id)
                form.save()

                return redirect('entry_app:main_app:song_detail', song_id=song_id)
            else:
                context['comment_form'] = comment_form
        else:
            comment_form = CommentForm(request.POST)
            context['comment_form'] = comment_form
            messages.success(request, "Success! Comment added")

        if Comment.objects.values('rating'):
            rating = Comment.objects.values('rating').aggregate(Avg('rating'))
        else:
            rating = None

        context = {'songs': songs,
                   'playlists': playlists,
                   'is_favourite': is_favourite,
                   'last_played': last_played_song,
                   'comments': comments,
                   'comment_form': comment_form,
                   'rating': rating,
                   }

        return render(request, 'main_app/detail.html', context)
    else:
        return redirect('entry_app:login')


def become_creator(request):
    if request.user.is_authenticated:
        if not request.user.is_creator:
            context = {}
            my_record = CustomUser.object.get(id=request.user.id)

            if request.POST:
                form = CreatorForm(request.POST, instance=my_record)
                if form.is_valid():
                    become = form.save(commit=False)
                    become.is_creator = True
                    become.save()

                    return redirect('entry_app:main_app:music')
                else:
                    context['creator_form'] = form
            else:
                form = CreatorForm(instance=my_record)
                context['creator_form'] = form
                messages.success(request, "Success! Now you are a creator!")
            return render(request, 'main_app/become_creator.html', context)

        else:
            return messages.success(request, "You are already a creator!")
    else:
        return redirect('entry_app:login')


def creator_profile(request):
    template_name = 'main_app/creator.html'
    context = {}

    if Song.objects.filter(creator=request.user):
        songs = Song.objects.filter(creator=request.user)
    else:
        songs = None

    context = {
        'songs': songs,
    }

    return render(request, template_name, context)


def song_delete(request, song_id):
    Song.objects.filter(id=song_id).delete()

    template_name = 'main_app/creator.html'
    context = {}

    if Song.objects.filter(creator=request.user):
        songs = Song.objects.filter(creator=request.user)
    else:
        songs = None

    context = {
        'songs': songs,
    }

    return render(request, template_name, context)


def add_song(request):
    if request.user.is_authenticated:
        if request.user.is_creator:
            context = {}

            if request.POST:
                form = UploadFrom(request.POST, request.FILES)
                if form.is_valid():
                    upload = form.save(commit=False)
                    upload.creator = request.user
                    upload.save()

                    return redirect('entry_app:main_app:creator_profile')
                else:
                    context['upload_form'] = form
            else:
                form = UploadFrom(request.FILES)

                last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
                if last_played_list:
                    last_played_id = last_played_list[0]['song_id']
                    last_played_song = Song.objects.get(id=last_played_id)
                else:
                    last_played_song = Song.objects.get(id=1)

                context = {'upload_form': form, 'last_played': last_played_song}
            return render(request, 'main_app/SongUpload.html', context)

        else:
            return HttpResponse("You are not creator!")
    else:
        return redirect('entry_app:login')


def playlist(request):
    if request.user.is_authenticated:
        last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            last_played_song = Song.objects.get(id=1)

        playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
        context = {'playlists': playlists, 'last_played': last_played_song}
        return render(request, 'main_app/playlist.html', context=context)
    else:
        return redirect("entry_app:login")


def playlist_songs(request, playlist_name):
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=1)

    songs = Playlist.objects.filter(playlist_name=playlist_name, user=request.user).distinct()

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(playlist_name=playlist_name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")

    context = {'playlist_name': playlist_name, 'songs': songs, 'last_played': last_played_song }

    return render(request, 'main_app/playlist_songs.html', context=context)



def favorite(request):
    if request.user.is_authenticated:
        last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            last_played_song = Song.objects.get(id=1)

        songs = Song.objects.filter(favorite__user=request.user, favorite__is_fav=True).distinct()
        print(f'songs: {songs}')

        if request.method == "POST":
            song_id = list(request.POST.keys())[1]
            favourite_song = Favorite.objects.filter(user=request.user, song__id=song_id, is_fav=True)
            favourite_song.delete()
            messages.success(request, "Removed from favourite!")

        context = {'songs': songs, 'last_played': last_played_song}
        return render(request, 'main_app/favorite.html', context=context)
    else:
        return redirect("entry_app:login")


def recent(request):
    if request.user.is_authenticated:
        last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            last_played_song = Song.objects.get(id=1)

        # Display recent songs
        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if recent and request.user.is_authenticated:
            recent_id = [each['song_id'] for each in recent]
            recent_songs_unsorted = Song.objects.filter(id__in=recent_id, recent__user=request.user)
            recent_songs = list()
            for id in recent_id:
                recent_songs.append(recent_songs_unsorted.get(id=id))
        else:
            recent_songs = None

        if len(request.GET) > 0:
            search_query = request.GET.get('q')
            filtered_songs = recent_songs_unsorted.filter(Q(song_name__icontains=search_query)).distinct()
            context = {'recent_songs': filtered_songs, 'last_played': last_played_song, 'query_search': True}
            return render(request, 'main_app/recent.html', context)

        context = {'recent_songs': recent_songs, 'last_played': last_played_song, 'query_search': False}
        return render(request, 'main_app/recent.html', context=context)
    else:
        return redirect("entry_app:login")


def play_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('entry_app:main_app:music')


def play_recent_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()

    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('entry_app:main_app:recent')
