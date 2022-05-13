from django.urls import path
from entry_app import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
]