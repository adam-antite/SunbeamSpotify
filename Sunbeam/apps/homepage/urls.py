from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authorize/', views.authorize, name='authorize'),
    path('login/', views.api_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('playlist_shuffle/', views.playlist_shuffle, name='playlist_shuffle'),
    path('daily_playlist', views.daily_playlist, name='daily_playlist')
]
