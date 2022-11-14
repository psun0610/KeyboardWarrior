from .models import Trades, Trade_Comment
from django import forms


class CreateTrade(forms.ModelForm):
    class Meta:
        model = Trades
        fields = ["title", "content", "Trade_type", "price", "img"]


class CreateComment(forms.ModelForm):
    class Meta:
        model = Trade_Comment
        fields = [
            "content",
        ]
