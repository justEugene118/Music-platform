from django.urls import path, include
from entry_app import views

app_name = 'entry_app'


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('login', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('music/', include(('main_app.urls', 'main_app'), namespace='main_app')),
]
