# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime
from .models import Room, Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

x = datetime.datetime.now()
connected_user = []


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, msg, room_pk, user_pk):
        return Message.objects.create(room_id=room_pk, user_id=user_pk, content=msg)

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        username = self.scope["user"].username
        if username in connected_user:
            pass
        else:
            connected_user.append(username)
            message = username + "님이 입장하셨습니다"
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "connected_user": len(connected_user),
                },
            )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        username = self.scope["user"].username
        if username not in connected_user:
            pass
        else:
            connected_user.remove(username)
            message = username + "님이 퇴장하셨습니다"
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "connected_user": len(connected_user),
                },
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        user = self.scope["user"]
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        room_pk = text_data_json["room_pk"]
        context = {
            "userid": user.pk,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "image": str(user.image),
            "is_social": user.is_social,
            "date": x.strftime("%m월 %d일 %H:%M"),
            "room_pk": room_pk,
        }
        new_msg = await self.create_chat(message, room_pk, user.pk)
        # print(user.pk, type(user.pk))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "context": context,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        user = self.scope["user"]
        context = {
            "userid": user.pk,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "image": str(user.image),
            "is_social": user.is_social,
            "connected_user": len(connected_user),
            "date": x.strftime("%m월 %d일 %H:%M"),
        }
        message = event["message"]
        # print(event, 123)
        room = event.get("context")
        room_pk = "0"
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "context": context,
                    "room_pk": room_pk,
                }
            )
        )
