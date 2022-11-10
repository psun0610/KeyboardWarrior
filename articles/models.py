from django.db import models
from KW.settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model

# Create your models here.

press_ = [(1, "가벼움"),
    (2, "무거움"),
    (3, "상관없음"),
]

array_ = [(1, "87")]

sound_ = [(1, "저소음")]

switch_ = [
    (1, "청축"),
]

connect_ = [(1, "유선"), (2, "무선")]


class Keyboard(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    article_like = models.ManyToManyField(
        AUTH_USER_MODEL, symmetrical=False, related_name="like_article"
    )
    mark = models.ManyToManyField(
        AUTH_USER_MODEL, symmetrical=False, related_name="marker"
    )
    img = models.ImageField(
        default="img/default_image.jpeg",
        upload_to="img/",
        blank=True,
    )
    name = models.CharField(max_length=80, blank=True)
    brand = models.CharField(max_length=50, blank=True)
    connect = models.CharField(max_length=50, blank=True)
    array = models.CharField(max_length=50, blank=True)
    switch = models.CharField(max_length=50, blank=True)
    key_switch = models.CharField(max_length=50, blank=True)
    press = models.CharField(max_length=50, blank=True)
    weight = models.CharField(max_length=50, blank=True)
