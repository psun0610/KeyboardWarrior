# chat/views.py
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.models import User
from django.utils.safestring import mark_safe
from trade.models import Trades
from reviews.models import Review
from .models import Message, Room
from django.db.models import Q
import json


def index(request):
    return render(request, "chat/index.html")


# @login_required
# def room(request, room_name):
#     user = User.objects.get(pk=request.user.pk)
#     username = user.username
#     userimg = user.image
#     context = {
#     "user": user,
#     "username": username,
# "user_pk": request.user.pk,
# "room_name": room_name,
# "userimg": userimg,
#     }

#     return render(request, "chat/room1.html", context)


@login_required
def room(request, room_name):
    send_user = request.user
    room = Room.objects.get(pk=room_name)
    all_room = Room.objects.filter(
        Q(send_user=request.user) | Q(reception_user=request.user)
    )
    room_message = Message.objects.filter(room=room)
    context = {
        "room": room,
        "room_name": room.pk,
        "user_pk": send_user.pk,
        "user": send_user,
        "room_message": room_message,
        "username": send_user.username,
        "userimg": send_user.image,
        "all_room": all_room,
    }

    return render(request, "chat/room1.html", context)


@login_required
def find_room(request, trade_pk):
    send_user = request.user
    trade = Trades.objects.get(pk=trade_pk)
    reception_user = trade.user

    # 만약 방이 이미 있으면 room.pk찾기
    if Room.objects.filter(
        trade=trade, send_user=send_user, reception_user=reception_user
    ).exists():
        select_room = Room.objects.filter(
            trade=trade, send_user=send_user, reception_user=reception_user
        )
        old_room = select_room[0]
        return redirect("chat:room", old_room.pk)
    # 방이 없다면 (최초 채팅 시행) room.pk 생성
    else:
        new_room = Room.objects.create(
            trade=trade,
            reception_user=reception_user,
            send_user=send_user,
        )
        return redirect("chat:room", new_room.pk)
