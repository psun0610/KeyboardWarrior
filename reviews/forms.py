from django import forms
from .models import Reviews, Comment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = {
            "title",
            "grade",
            "content",
            "img",
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = {'content', }