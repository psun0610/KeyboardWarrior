# chat/views.py
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from accounts.models import Notification
from django.utils.safestring import mark_safe
from trade.models import Trades
from reviews.models import Review
from .models import Message, Room
from django.db.models import Q
import json
from django.db.models.signals import post_save

from django.http import JsonResponse
from datetime import datetime


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
    if room.reception_user == request.user or room.send_user == request.user:
        all_room = Room.objects.filter(
            Q(send_user=request.user) | Q(reception_user=request.user)
        )
        room_message = Message.objects.filter(room=room)
        if request.user.is_authenticated:
            new_message = Notification.objects.filter(
                Q(user=request.user) & Q(check=False)
            )
            message_count = len(new_message)
            context = {
                "count": message_count,
                "room": room,
                "room_name": room.pk,
                "user_pk": send_user.pk,
                "user": send_user,
                "room_message": room_message,
                "username": send_user.username,
                "userimg": send_user.image,
                "all_room": all_room,
            }
        else:
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
        return render(request, "chat/room.html", context)
    else:
        return redirect("articles:main")


@login_required
# @receiver(post_save, sender=User)
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
        message = f"{new_room.trade.title}의 거래글에 대화가 도착했습니다"
        Notification.objects.create(
            user=new_room.trade.user, message=message, category="채팅", nid=new_room.pk
        )
        return redirect("chat:room", new_room.pk)


def message(request):
    roompk = request.GET.get("room")
    content = request.GET.get("content")
    if content == "내용없음":
        room = Room.objects.get(pk=roompk)
        room_message_fil = Message.objects.filter(room=room.pk).order_by("pk")
        room_message = []
        for m in room_message_fil:
            room_message.append(
                {
                    "msg": m.content,
                    "username": m.user.username,
                    "userpk": m.user.pk,
                    "created_at": m.created_at.strftime("%Y-%m-%d %H:%M"),
                }
            )
        context = {
            "room_message": room_message,
        }
        return JsonResponse(context)
    else:
        room = Room.objects.get(pk=roompk)
        Message.objects.create(user=request.user, content=content, room=room)
        room_message_fil = Message.objects.filter(room=room.pk).order_by("pk")
        room_message = []
        for m in room_message_fil:
            room_message.append(
                {
                    "msg": m.content,
                    "username": m.user.username,
                    "userpk": m.user.pk,
                    "created_at": m.created_at.strftime("%Y-%m-%d %H:%M"),
                }
            )
        context = {
            "room_message": room_message,
        }
        return JsonResponse(context)


@login_required
def init_room(request):
    user = request.user
    # 만약 방이 이미 있으면 room.pk찾기
    if Room.objects.filter(Q(send_user=user) | Q(reception_user=user)).exists():

        select_room = Room.objects.filter(Q(send_user=user) | Q(reception_user=user))

        room = select_room.order_by("pk")[0]

        return redirect("chat:room", room.pk)

    # 방이 없다면 (최초 채팅 시행) room.pk 생성
    else:
        return render(request, "chat/empty.html")
