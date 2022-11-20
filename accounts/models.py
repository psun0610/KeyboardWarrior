from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from KW.settings import AUTH_USER_MODEL
from trade.models import Trades


# Create your models here.

#
Key_Press = [
    (1, "가벼움"),
    (2, "무거움"),
    (3, "상관없음"),
]
Array = [
    (1, "풀배열"),
    (2, "텐키리스"),
    (3, "상관없음"),
]
Sound = [
    (1, "경쾌한 소리"),
    (2, "조용한 소리"),
    (3, "상관없음"),
]
Weight = [
    (1, "가벼움"),
    (2, "상관없음"),
]
connect = [
    (1, "유선"),
    (2, "무선"),
    (3, "상관없음"),
]


class User(AbstractUser):
    naver_id = models.CharField(null=True, unique=True, max_length=100)
    goo_id = models.CharField(null=True, unique=True, max_length=50)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    press = MultiSelectField(choices=Key_Press, null=True)
    weight = MultiSelectField(choices=Weight, null=True)
    array = MultiSelectField(choices=Array, null=True)
    sound = MultiSelectField(choices=Sound, null=True)
    rank = models.IntegerField(default=0)
    connect = MultiSelectField(choices=connect, null=True)
    image = ProcessedImageField(
        blank=True,
        processors=[Thumbnail(300, 300)],
        format="jpeg",
        options={"quality": 90},
    )
    # 기본 0 구글 1 네이버 2
    is_social = models.IntegerField(default=0)



class Notification(models.Model):
    message = models.CharField(max_length=100)
    check = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10)
    nid = models.IntegerField(default=0)
