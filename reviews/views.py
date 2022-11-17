from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm, PhotoForm
from .models import Review, Comment, Photo
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe
from django.http import JsonResponse
from accounts.models import User
from datetime import date, datetime, timedelta
from articles.models import Keyboard
from django.db.models import Count
from django.db.models import Q
def maketable(p):
    table = [0] * len(p)
    i = 0
    for j in range(1, len(p)):
        while i > 0 and p[i] != p[j]:
            i = table[i - 1]
        if p[i] == p[j]:
            i += 1
            table[j] = i
    return table


def KMP(p, t):
    ans = []
    table = maketable(p)
    i = 0
    for j in range(len(t)):
        while i > 0 and p[i] != t[j]:
            i = table[i - 1]
        if p[i] == t[j]:
            if i == len(p) - 1:
                ans.append(j - len(p) + 2)
                i = table[i]
            else:
                i += 1
    return ans


# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-pk")
    photo_list = []
    for review in reviews:
        if review.photo_set.all():
            thumbnail = review.photo_set.all()[0]
            photo_list.append((thumbnail, review.photo_set.all().count()))
    context = {
        "photo_list": photo_list,
    }
    return render(request, "reviews/index.html", context)


# 리뷰작성
@login_required
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        kb = Keyboard.objects.get(name=request.POST["keyboard"])
        if review_form.is_valid() and photo_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.keyboard = kb
            if len(images):
                for image in images:
                    image_instance = Photo(review=review, image=image)
                    review.save()
                    image_instance.save()
            else:
                review.save()
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
        photo_form = PhotoForm()
    context = {
        "review_form": review_form,
        "photo_form": photo_form,
    }
    return render(request, "reviews/create.html", context)


# 리뷰 읽기
def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comments = Comment.objects.filter(review_id=pk).order_by("-pk")
    comment_form = CommentForm()
    photos = review.photo_set.all()
    for t in comments:
        with open("filtering.txt") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )
    comment_form.fields["content"].widget.attrs["placeholder"] = "댓글 작성"
    context = {
        "review": review,
        "comments": comments,
        "comment_form": comment_form,
        "photos": photos,
    }
    response = render(request, "reviews/detail.html", context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookievalue = request.COOKIES.get("hitreview", "")

    if f"{pk}" not in cookievalue:
        cookievalue += f"{pk}"
        response.set_cookie(
            "hitreview", value=cookievalue, max_age=max_age, httponly=True
        )
        review.hits += 1
        review.save()
    return response


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
        if request.user not in t.like_users.all():
            is_like = True
        else:
            is_like = False
        t.created_at = t.created_at.strftime("%Y-%m-%d %H:%M")
        with open("filtering.txt") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )
            comment_data.append(
                {
                    "id": t.user_id,
                    "userName": t.user.username,
                    "content": t.content,
                    "commentPk": t.pk,
                    "created_at": t.created_at,
                    "islike": is_like,
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
        if request.user not in t.like_users.all():
            is_like = True
        else:
            is_like = False
        t.created_at = t.created_at.strftime("%Y-%m-%d %H:%M")
        with open("filtering.txt") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )
        comment_data.append(
            {
                "id": t.user.pk,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "created_at": t.created_at,
                "islike": is_like,
            }
        )
    context = {
        "comment_data": comment_data,
        "review_pk": review_pk.pk,
        "user": user.pk,
    }
    return JsonResponse(context)


# 좋아요
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


# 댓글 좋아요
def comment_like(request, review_pk, comment_pk):
    is_like = False
    temp = Comment.objects.filter(review_id=review_pk)
    for i in temp:
        if i.pk == comment_pk:
            if request.user not in i.like_users.all():
                i.like_users.add(request.user)
                is_like = True
            else:
                i.like_users.remove(request.user)
                is_like = False
            data = {
                "review.pk": review_pk,
                "comment_pk": comment_pk,
                "isLike": is_like,
            }
            return JsonResponse(data)


# 즐겨찾기(bookmark)
def bookmark(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user not in review.bookmark_users.all():
        review.bookmark_users.add(request.user)
        is_bookmark = True
    else:
        review.bookmark_users.remove(request.user)
        is_bookmark = False
    context = {
        "isBookmark": is_bookmark,
    }
    return JsonResponse(context)

# 후기 검색
def review_search(request):
    if 'kw' in request.GET:
        # kw = index.html의 검색창 input의 name이다.
        search_word = request.GET.get("kw")
        reviews = Review.objects.filter(
            Q(title__icontains=search_word) |
            Q(content__icontains=search_word) |
            Q(keyboard__name__icontains=search_word) |
            Q(user__username__icontains=search_word)
        ).order_by("-pk")
        photo_list = []
        for review in reviews:
            if review.photo_set.all():
                thumbnail = review.photo_set.all()[0]
                photo_list.append((thumbnail, review.photo_set.all().count()))
        context = {
            "reviews": reviews,
            "search_word": search_word,
            "photo_list": photo_list,
        }
        return render(request, 'reviews/index.html', context)
    else:
        return render(request, 'reviews/index.html')




def best(request, pk):
    reviews = Review.objects.filter(keyboard_id=pk).annotate(num_=Count("like_users")).order_by("-num_")
    photo_list = []
    for review in reviews:
        if review.photo_set.all():
            thumbnail = review.photo_set.all()[0]
            photo_list.append((thumbnail, review.photo_set.all().count()))
    context = {
        "photo_list": photo_list,
    }
    return render(request, "reviews/index.html", context)

