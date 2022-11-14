from .models import Trades, Trade_Comment, Photo
from django import forms
from django.forms import ClearableFileInput

class CreateTrade(forms.ModelForm):
    class Meta:
        model = Trades
        fields = ["title", "content", "Trade_type", "price"]

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("image",)
        widgets = {
            "image": ClearableFileInput(attrs={"multiple": True}),
        }
        labels = {
            "image": "사진을 여러장 올릴 수 있어요! 첫장은 썸네일~",
        }

class CreateComment(forms.ModelForm):
    class Meta:
        model = Trade_Comment
        fields = [
            "content",
        ]
