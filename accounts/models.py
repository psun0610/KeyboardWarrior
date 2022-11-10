from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField


# Create your models here.

# 
Key_Press = [

    (1, "38"),
    (2, "45"),
    (3, "상관없음"),

]
Array = [
    (1, "ten"),
    (2, "tenkeyless"),
    (3, "상관없음"),
]
Sound =[
    (1, "소음"),
    (2, "저소음"),
    (3, "상관없음"),
]
Weight = [
    (1, "가벼움"),
    (2, "상관없음"),

]
connect = [
    (1, "유"),
    (2, "무"),
    (3, "상관없음"),
]
class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    press = MultiSelectField(choices=Key_Press)
    weight = MultiSelectField(choices=Weight)
    array = MultiSelectField(choices=Array)
    sound = MultiSelectField(choices=Sound)
    rank = models.IntegerField(default=0)
    connect = MultiSelectField(choices=connect)