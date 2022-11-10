from django import forms
from .models import Reviews


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = {
            "title",
            "grade",
            "content",
            "img",
        }