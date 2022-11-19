# chat/views.py
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.models import User
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, "chat/index.html")
@login_required
def room(request, room_name):
    user = User.objects.get(pk=request.user.pk)
    username = user.username
    userimg = user.image
    context = {
        "user":user,
        "room_name": room_name,
        "username": username,
        "user_pk": request.user.pk,
        "userimg":userimg,
    }
    return render(request, "chat/room.html", context)