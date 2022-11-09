from django.db import models
from KW.settings import AUTH_USER_MODEL

# Create your models here.

tradeType = [(1, "팝니다"), (2, "삽니다")]


class Trades(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    Trade_type = models.IntegerField(choices=tradeType)
    title = models.CharField(max_length=80)
    content = models.TextField(max_length=500)
