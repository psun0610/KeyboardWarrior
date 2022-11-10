from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from .models import Reviews
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


def index(request):
    reviews = Reviews.objects.order_by("-pk")
    context = {
        "reviews": reviews,
    }
    return render(request, "reviews/index.html", context)

#리뷰작성
@login_required
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/create.html", context)

# 리뷰 읽기
def detail(request, pk):
    review = Reviews.objects.get(pk=pk)
    context = {
        "review": review,
    }

    return render(request, "reviews/detail.html", context)

# 리뷰 수정
@login_required
def update(request, pk):
    review = Reviews.objects.get(pk=pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("reviews:detail", pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {
        "review_form": review_form,
        "review": review,
    }
    return render(request, "reviews/update.html", context)

# 리뷰 삭제
@login_required
def delete(request, pk):
    review = Reviews.objects.get(pk=pk)  # 어떤 글인지
    review.delete()
    return redirect("reviews:index")