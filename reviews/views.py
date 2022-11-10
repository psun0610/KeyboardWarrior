from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Reviews
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe
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
    reviews = get_object_or_404(Reviews, pk=pk)
    comment_form = CommentForm()
    context = {
        'review': reviews,
        'comments': reviews.comment_set.all(),
        'comment_form': comment_form,
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

# 댓글 생성
@login_required
def comment_create(request, pk):
    print(request.POST)
    review = get_object_or_404(Reviews, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        context = {
            'content': comment.content,
            'userName': comment.user.username
        }
        return JsonResponse(context)

# 댓글생성
# @login_required(login_url="accounts:login")
# def comment_create(request, pk):
#     review = Reviews.objects.get(pk=pk)
#     users = User.objects.get(pk=request.user.pk)
#     users.rank += 1
#     users.save()

#     comment_form = CommentForm(request.POST)
#     user = request.user.pk
#     if comment_form.is_valid():
#         comment = comment_form.save(commit=False)
#         comment.review = review
#         comment.user = request.user
#         comment.save()
#     # 제이슨은 객체 형태로 받질 않음 그래서 리스트 형태로 전환을 위해 리스트 생성
#     temp = Comment.objects.filter(review_id=pk).order_by("-pk")
#     comment_data = []
#     for t in temp:
#         t.created_at = t.created_at.strftime("%Y-%m-%d %H:%M")
#         comment_data.append(
#             {
#                 "id": t.user_id,
#                 "userName": t.user.username,
#                 "content": t.content,
#                 "commentPk": t.pk,
#                 "created_at": t.created_at,
#                 "profile_name": t.user.profile_name,
#                 "profile_image": t.user.profile_image.url,
#             }
#         )
#     context = {
#         "comment_data": comment_data,
#         "review_pk": pk,
#         "user": user,
#     }
#     return JsonResponse(context)