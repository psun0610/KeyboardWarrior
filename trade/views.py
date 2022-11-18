from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CreateTrade, CreateComment, PhotoForm
from .models import Trades, Trade_Comment, Photo
from accounts.models import User
from django.http import JsonResponse
from articles.models import Keyboard
from datetime import date, datetime, timedelta
from reviews.models import Review
from django.db.models import Count
from django.db.models import Q

# Create your views here.


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


def index(request):
    trades = Trades.objects.order_by("-pk")
    photo_list = []

    context = {
        "photo_list": photo_list,
        "trades": trades,
    }
    return render(request, "trade/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = CreateTrade(request.POST, request.FILES)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        kb = Keyboard.objects.get(name=request.POST["keyboard"])
        if form.is_valid() and photo_form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user
            trade.keyboard = kb
            if len(images):
                for image in images:
                    image_instance = Photo(trade=trade, image=image)
                    trade.save()
                    image_instance.save()
            else:
                trade.save()
            return redirect("trade:index")
    else:
        form = CreateTrade()
        photo_form = PhotoForm()
    context = {
        "form": form,
        "photo_form": photo_form,
    }
    return render(request, "trade/create.html", context)


@login_required
def update(request, pk):
    trade = get_object_or_404(Trades, pk=pk)
    if request.user == trade.user:
        if request.method == "POST":
            form = CreateTrade(request.POST, instance=trade)
            if form.is_valid():
                trade = form.save(commit=False)
                trade.user = request.user
                trade.save()
                return redirect("trade:detail", pk)
        else:
            form = CreateTrade(instance=trade)
        context = {
            "form": form,
        }
    return render(request, "trade/update.html", context)


def detail(request, pk):
    trade = get_object_or_404(Trades, pk=pk)
    reviews = Review.objects.all()
    photos = trade.photo_set.all()
    comments = Trade_Comment.objects.filter(trade=pk).order_by("-pk")
    comment_form = CreateComment()
    for c in comments:
        with open("filtering.txt") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, c.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(c.content) // 2:
                            c.content = (
                                len(c.content[k - 1 : len(word)]) * "*"
                                + c.content[len(word) :]
                            )
                        else:
                            c.content = (
                                c.content[0 : k - 1] + len(c.content[k - 1 :]) * "*"
                            )
    total = 0
    cnt = 0
    aval = 0.0
    for review in reviews:
        if trade.keyboard_id == review.keyboard_id:
            total += review.grade
            cnt += 1
    if cnt:
        aval = round(total / cnt, 1)
    context = {
        "trade": trade,
        "photos": photos,
        "comment_form": comment_form,
        "comments": comments,
        "aval": aval,
    }
    return render(request, "trade/detail.html", context)


@login_required
def delete(request, pk):
    trade = get_object_or_404(Trades, pk=pk)
    if request.user == trade.user:
        trade.delete()
    return redirect("trade:index")


@login_required
def marker(request, pk):
    trade = Trades.objects.get(pk=pk)
    is_marker = True
    if request.user != trade.user:
        if request.user not in trade.marker.all():
            trade.marker.add(request.user)
            is_marker = True
        else:
            trade.marker.remove(request.user)
            is_marker = False
    data = {
        "markers": trade.marker.all().count(),
        "is_marker": is_marker,
    }
    return JsonResponse(data)


@login_required
def trade_comment(request, pk):
    users = User.objects.get(pk=request.user.pk)
    users.rank += 2
    users.save()
    trade_ = get_object_or_404(Trades, pk=pk)
    if request.method == "POST":
        form = CreateComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.trade = trade_
            comment.save()
        comments = Trade_Comment.objects.filter(trade=trade_).order_by("-pk")
        user = request.user
        comment_list = []
        for c in comments:
            with open("filtering.txt") as txtfile:
                for word in txtfile.readlines():
                    word = word.strip()
                    ans = KMP(word, c.content)
                    if ans:
                        for k in ans:
                            k = int(k)
                            if k < len(c.content) // 2:
                                c.content = (
                                    len(c.content[k - 1 : len(word)]) * "*"
                                    + c.content[len(word) :]
                                )
                            else:
                                c.content = (
                                    c.content[0 : k - 1] + len(c.content[k - 1 :]) * "*"
                                )
            comment_list.append(
                {
                    "username": c.user.username,
                    "content": c.content,
                    "create_at": c.create_at,
                    "user_pk": c.user.pk,
                    "comment_pk": c.pk,
                    "image": str(c.user.image),
                    "is_social": c.user.is_social,
                }
            )
        context = {
            "comment_list": comment_list,
            "user": user.pk,
            "trade": trade_.pk,
        }
        return JsonResponse(context)


@login_required
def delete_comment(request, trade_pk, comment_pk):
    comment = get_object_or_404(Trade_Comment, pk=comment_pk)
    trade_ = get_object_or_404(Trades, pk=trade_pk)
    if request.user == comment.user:
        comment.delete()
        comments = Trade_Comment.objects.filter(trade=trade_).order_by("-pk")
        user = request.user
        comment_list = []
        for c in comments:
            with open("filtering.txt") as txtfile:
                for word in txtfile.readlines():
                    word = word.strip()
                    ans = KMP(word, c.content)
                    if ans:
                        for k in ans:
                            k = int(k)
                            if k < len(c.content) // 2:
                                c.content = (
                                    len(c.content[k - 1 : len(word)]) * "*"
                                    + c.content[len(word) :]
                                )
                            else:
                                c.content = (
                                    c.content[0 : k - 1] + len(c.content[k - 1 :]) * "*"
                                )

            comment_list.append(
                {
                    "username": c.user.username,
                    "content": c.content,
                    "create_at": c.create_at,
                    "user_pk": c.user.pk,
                    "comment_pk": c.pk,
                    "image": str(c.user.image),
                    "is_social": c.user.is_social,
                }
            )
        context = {
            "comment_list": comment_list,
            "user": user.pk,
        }
    return JsonResponse(context)


def keyboard_search(request):
    search_data = request.GET.get("search", "")
    keyboard = Keyboard.objects.filter(name__icontains=search_data).all()
    keyboard_list = []
    for k in keyboard:
        keyboard_list.append(
            {
                "name": k.name,
                "img": k.img,
                "brand": k.brand,
                "id": k.pk,
            }
        )
    context = {
        "keyboard_list": keyboard_list,
    }
    return JsonResponse(context)


# 마켓 검색기능
def trade_search(request):
    if "kw" in request.GET:
        # kw = index.html의 검색창 input의 name이다.
        search_word = request.GET.get("kw")
        trades = Trades.objects.filter(
            Q(title__icontains=search_word)
            | Q(content__icontains=search_word)
            | Q(keyboard__name__icontains=search_word)
            | Q(user__username__icontains=search_word)
        )
        photo_list = []
        for trade in trades:
            if trade.photo_set.all():
                thumbnail = trade.photo_set.all()[0]
                photo_list.append(thumbnail)
        context = {
            "trades": trades,
            "search_word": search_word,
            "photo_list": photo_list,
        }
        return render(request, "trade/index.html", context)


def send_market(request, pk):
    pick_data = Trades.objects.filter(keyboard=pk)
    photo_list = []
    for trade in pick_data:
        if trade.photo_set.all():
            thumbnail = trade.photo_set.all()[0]
            photo_list.append(thumbnail)

    context = {"photo_list": photo_list}

    return render(request, "trade/index.html", context)


@login_required
def status(request, pk):
    trade = Trades.objects.get(pk=pk)
    is_done = True
    if request.user == trade.user:
        if trade.status_type == 1:
            trade.status_type = 2
            is_done = True
            trade.save()
        else:
            trade.status_type = 1
            is_done = False
            trade.save()
    context = {
        "is_done": is_done,
    }
    return JsonResponse(context)
