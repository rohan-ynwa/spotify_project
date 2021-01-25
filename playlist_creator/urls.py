from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('music', views.music, name="music-page")
]

