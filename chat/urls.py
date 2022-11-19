# chat/urls.py
from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.index, name="index"),
    # path("<str:trade_pk>/", views.room, name="room"),
    path("<str:room_name>/", views.room, name="room"),
    path("<int:trade_pk>/find_room/", views.find_room, name="find_room"),
]
