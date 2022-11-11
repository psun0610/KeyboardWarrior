from django.db import models
from KW.settings import AUTH_USER_MODEL

# Create your models here.

tradeType = [(1, "팝니다"), (2, "삽니다")]


# 가격추가 # 키보드 FK넣기


class Trades(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    Trade_type = models.IntegerField(choices=tradeType)
    title = models.CharField(max_length=80)
    content = models.TextField(max_length=500)


class Trade_Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trades, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
