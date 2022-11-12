from django.shortcuts import render, redirect

# Create your views here.


def main(request):
    return render(request, "articles/main.html")


def all(request):
    return render(request, "articles/all.html")

def detail(request):
    
    li = [1,2,3]
    context = {
        'li' : li,
    }
    return render(request, "articles/detail.html", context)

