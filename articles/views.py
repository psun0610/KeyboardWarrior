from django.shortcuts import render, redirect

# Create your views here.


def main(request):
    return render(request, "articles/main.html")


def all(request):
    return render(request, "articles/all.html")
