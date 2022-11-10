from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField


# Create your models here.

Key_Press = [
    (1, "35"),
    (2, "38"),
    (3, "45"),
    (4, "50"),
    (5, "55"),
    (6, "기타"),
]
Array = [
    (1, "87"),
    (2, "104"),
    (3, "108"),
    (4, "112"),
    (5, "120"),
    (6, "기타"),
]
Sound =[
    (1, "청축"),
    (2, "갈축"),
    (3, "은축"),
    (4, "적축"),
    (5, "흑축"),
    (6, "저소음"),
    (7, "기타"),
]
Weight = [
    (1, "500~600"),
    (2, "601~700"),
    (3, "701~800"),
    (4, "801~900"),
    (5, "901~1000"),
    (6, "1001~1100"),
    (7, "기타"),
]
class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    press = MultiSelectField(choices=Key_Press)
    weight = MultiSelectField(choices=Weight)
    array = MultiSelectField(choices=Array)
    sound = MultiSelectField(choices=Sound)
    rank = models.IntegerField(default=0)