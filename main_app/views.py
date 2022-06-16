from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.


def main_view(request):
    template_name = 'main_app/main.html'
    context = {}

    if request.user.is_authenticated:
        return render(request, template_name, context)
    else:
        return redirect('entry_app:login')


def player_view(request):
    pass
