from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe
from django.http import JsonResponse
from accounts.models import User

# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-pk")
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
    reviews = get_object_or_404(Review, pk=pk)
    comments = Comment.objects.filter(review_id=pk)
    comment_form = CommentForm()
    comment_form.fields["content"].widget.attrs["placeholder"] = "댓글 작성"
    context = {
        'review': reviews,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, "reviews/detail.html", context)

# 리뷰 수정
@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
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
    review = Review.objects.get(pk=pk)  # 어떤 글인지
    review.delete()
    return redirect("reviews:index")

# 댓글 생성
@login_required
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    users = User.objects.get(pk=request.user.pk)
    users.rank += 1
    users.save()

    comment_form = CommentForm(request.POST)
    user = request.user.pk
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    # 제이슨은 객체 형태로 받질 않음 그래서 리스트 형태로 전환을 위해 리스트 생성
    temp = Comment.objects.filter(review_id=pk).order_by("-pk")
    comment_data = []
    for t in temp:
        t.created_at = t.created_at.strftime("%Y-%m-%d %H:%M")
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "created_at": t.created_at,
            }
        )
    context = {
        "comment_data": comment_data,
        "review_pk": pk,
        "user": user,
    }
    return JsonResponse(context)

# 댓글 삭제
@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    review_pk = Review.objects.get(pk=review_pk)
    comment.delete()
    temp = Comment.objects.filter(review_id=review_pk).order_by("-pk")
    user = request.user
    comment_data = []
    for t in temp:
        t.created_at = t.created_at.strftime("%Y-%m-%d %H:%M")
        comment_data.append(
            {
                "id": t.user.pk,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "created_at": t.created_at,
            }
        )
    context = {
        "comment_data": comment_data,
        "review_pk": review_pk.pk,
        "user": user.pk,
    }
    return JsonResponse(context)

#좋아요
def like(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user not in review.like_users.all():
        review.like_users.add(request.user)
        is_like = True
    else:
        review.like_users.remove(request.user)
        is_like = False

    data = {
        "isLike": is_like,
        "likeCount": review.like_users.count(),
    }

    return JsonResponse(data)