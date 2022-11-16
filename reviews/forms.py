from django import forms
from .models import Review, Comment, Photo
from django.forms import ClearableFileInput

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = {
            "title",
            "grade",
            "content",
        }
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("image",)
        widgets = {
            "image": ClearableFileInput(attrs={"multiple": True}),
        }
        labels = {
            "image": "이미지를 선택해주세요.",
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            "content",
        }
