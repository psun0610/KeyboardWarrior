from django.db import models
from articles.models import Keyboard
from KW.settings import AUTH_USER_MODEL
# Create your models here.

grade_ = [(1, "★"), (2, "★★"), (3, "★★★"), (4, "★★★★"), (5, "★★★★★")]


class Review(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    content = models.TextField(max_length=500)
    grade = models.IntegerField(choices=grade_)
    img = models.ImageField(
        upload_to="img/",
        blank=True,
    )
    like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name='like_review')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.CharField(max_length=80)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    