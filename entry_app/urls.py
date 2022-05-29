from django.urls import path
from entry_app import views


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('login', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
