from django.db import models
from KW.settings import AUTH_USER_MODEL
from articles.models import Keyboard

# Create your models here.

tradeType = [(1, "팝니다"), (2, "삽니다")]
statusType = [(1, "거래중"), (2, "거래완료")]

# 가격추가 # 키보드 FK넣기


class Trades(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    Trade_type = models.IntegerField(choices=tradeType)
    title = models.CharField(max_length=80)
    content = models.TextField(max_length=500)
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    marker = models.ManyToManyField(
        AUTH_USER_MODEL, symmetrical=False, related_name="jjim"
    )
    status_type = models.IntegerField(choices=statusType, default=1)


class Photo(models.Model):
    trade = models.ForeignKey(Trades, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/", blank=True)


class Trade_Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trades, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
