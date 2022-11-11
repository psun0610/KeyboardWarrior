from django.db import models
from KW.settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model

# Create your models here.


class Keyboard(models.Model):
    name = models.CharField(max_length=80, blank=True)
    img = models.CharField(max_length=300, blank=True)
    brand = models.CharField(max_length=50, blank=True)
    connect = models.CharField(max_length=50, blank=True)
    array = models.CharField(max_length=50, blank=True)
    switch = models.CharField(max_length=50, blank=True)
    key_switch = models.CharField(max_length=50, blank=True)
    press = models.CharField(max_length=50, blank=True)
    weight = models.CharField(max_length=50, blank=True)
    kind = models.CharField(max_length=50, blank=True)
