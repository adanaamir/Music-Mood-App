from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),   # "" refers to what comes after the / (SpotifyMusic/)
    path("<str:name>", views.greet, name="greet"),
    path("adan", views.adan, name="adan"),   #here adan will come after / = (SpotifyMusic/adan)
]