from django.db import models
from KW.settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model

# Create your models here.

press_ = [(1, "가벼움")]

array_ = [(1, "텐키리스")]

sound_ = [(1, "저소음")]

switch_ = [(1, "청축")]

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
    title = models.CharField(max_length=80)
    content = models.TextField(max_length=500)
    press = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    array = models.CharField(max_length=50)
    sound = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    switch = models.CharField(max_length=50)
    connect = models.IntegerField(choices=connect_)
