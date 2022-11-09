from django.db import models
from articles.models import Keyboard
from KW.settings import AUTH_USER_MODEL

# Create your models here.

grade_ = [(1, "★"), (2, "★★"), (3, "★★★"), (4, "★★★★"), (5, "★★★★★")]


class Reviews(models.Model):
    article = models.ForeignKey(Keyboard, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    content = models.TextField(max_length=500)
    grade = models.IntegerField(choices=grade_)


class Comment(models.Model):
    content = models.CharField(max_length=80)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Keyboard, on_delete=models.CASCADE)
