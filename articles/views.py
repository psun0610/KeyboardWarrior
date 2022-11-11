from django.shortcuts import render, redirect
from .models import Keyboard
# Create your views here.


def main(request):
    return render(request, "articles/main.html")


def all(request):
    return render(request, "articles/all.html")