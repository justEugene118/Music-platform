from django import forms
from .models import *
from users_app.models import CustomUser


class UploadFrom(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_name', 'audio_file', 'genres', 'image_file', 'data_created']
        exclude = ['creator']

    widgets = {
        'audio_file': forms.FileInput(),
    }


class CreatorForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['creator_name', 'creator_descr']
        exclude = ['is_creator']

    widgets = {
        'creator_name': forms.CharField(),
        'creator_descr': forms.TextInput(),
    }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        exclude = ['user', 'song', 'date']

    widgets = {
        'text': forms.CharField(),
        'rating': forms.IntegerField()
    }
