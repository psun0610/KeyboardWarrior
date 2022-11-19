from .models import Message
from django import forms


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "content",
        ]
        labels = {
            "content": "내용",
        }
