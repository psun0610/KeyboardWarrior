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
    print(send_user.pk, 333)
    trade = Trades.objects.get(pk=int(room_name))
    reception_user = trade.user

    # 만약 방이 이미 있으면
    if Room.objects.filter(
        trade=trade, send_user=send_user, reception_user=reception_user
    ).exists():
        select_room = Room.objects.filter(
            trade=trade, send_user=send_user, reception_user=reception_user
        )
        old_room = select_room[0]
        all_room = Room.objects.filter(
            Q(send_user=request.user) | Q(reception_user=request.user)
        )
        room_message = Message.objects.filter(room=old_room)
        context = {
            "room_name": old_room.pk,
            "user_pk": send_user.pk,
            "user": send_user,
            "room_message": room_message,
            "username": send_user.username,
            "userimg": send_user.image,
            "all_room": all_room,
        }

    # 첫 메세지 전송이라면 (방이 없다면)
    else:
        new_room = Room.objects.create(
            trade=trade,
            reception_user=reception_user,
            send_user=send_user,
        )
        all_room = Room.objects.filter(
            Q(send_user=request.user) | Q(reception_user=request.user)
        )

        room_message = Message.objects.filter(room=new_room)

        context = {
            # "room_name": new_room.pk,
            # "user": send_user,
            # "all_room": all_room,
            # "room_message": room_message,
            "room_name": old_room.pk,
            "user_pk": send_user.pk,
            "user": send_user,
            "room_message": room_message,
            "username": send_user.username,
            "userimg": send_user.image,
            "all_room": all_room,
        }

    return render(request, "chat/room1.html", context)


# @login_required
# def room(request, room_name):
#     team = Team.objects.get(ename=room_name)
#     team_img = Team.objects.get(pk=request.user.team_id).logo.url
#     context = {
#         "room_name": room_name,
#         "team": team,
#         "team_img": mark_safe(json.dumps(team_img)),
#         "user_pk": request.user.pk,
#         "username": request.user.nickname,
#     }
#     return render(request, "chat/room.html", context)
