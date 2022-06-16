from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from .forms import SignUpForm, LogInForm
from django.contrib.auth import login, authenticate, logout
import main_app.urls

'''
    Templates can be visually upgraded, can be taken from here:
    https://github.com/SelmiAbderrahim/Authentication-Pages
    
    Best guide for whole application:
    https://www.youtube.com/watch?v=tTvSl3RHBjE&list=PLgCYzUzKIBE_dil025VAJnDjNZHHHR9mW&index=16
'''


# Create your views here
class MainView(TemplateView):
    template_name = 'entry_app/main.html'

    user = settings.AUTH_USER_MODEL

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('entry_app:main_app:music')
        else:
            return render(request, self.template_name, {})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('entry_app:main_app:music')
    else:
        context = {}
        user = request.user

        if user.is_authenticated:
            return redirect('entry_app:main_app:music')

        if request.POST:
            form = LogInForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']

                user = authenticate(email=email, password=password)

                if user:
                    login(request, user)
                    return redirect('entry_app:main_app:music')
        else:
            form = LogInForm()

        context['login_form'] = form
        return render(request, 'entry_app/login.html', context)


def logout_view(request):
    logout(request)

    return redirect('entry_app:main')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('entry_app:main_app:music')
    else:
        context = {}
        if request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()

                email = form.cleaned_data.get('form')
                raw_password = form.cleaned_data.get('password1')
                new_user = authenticate(email=email, password=raw_password)

                login(request, new_user)
                return redirect('entry_app:main_app:music')
            else:
                context['signup_form'] = form
        else:
            form = SignUpForm()
            context['signup_form'] = form
        return render(request, 'entry_app/signup.html', context)
