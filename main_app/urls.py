from django.urls import path, include
from main_app import views

app_name = 'main_app'


urlpatterns = [
    path('', views.main_view, name="music"),

]
