from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField


# Create your models here.

press_ = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
]


class User(AbstractUser):
    followings = (
        models.ManyToManyField("self", symmetrical=False, related_name="follower"),
    )
    press = MultiSelectField(choices=press_)
    weight = MultiSelectField(choices=press_)
    array = MultiSelectField(choices=press_)
    sound = MultiSelectField(choices=press_)
