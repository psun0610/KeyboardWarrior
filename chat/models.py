from django.db import models
from KW.settings import AUTH_USER_MODEL
from trade.models import Trades


class Room(models.Model):
    send_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    reception_user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="받는사람"
    )
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)
    trade = models.ForeignKey(Trades, on_delete=models.CASCADE)


class Message(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
