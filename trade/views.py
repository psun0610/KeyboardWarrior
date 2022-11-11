from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateTrade, CreateComment
from .models import Trades, Trade_Comment
from django.http import JsonResponse

# Create your views here.


def index(request):
    trades = Trades.objects.all()
    context = {"trades": trades}
    return render(request, "trade/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = CreateTrade(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user
            trade.save()
            return redirect("trade:index")
    else:
        form = CreateTrade()
    context = {
        "form": form,
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
    comments = Trade_Comment.objects.filter(trade=pk).order_by("-pk")
    comment_from = CreateComment()
    context = {
        "trade": trade,
        "comment_from": comment_from,
        "comments": comments,
    }
    return render(request, "trade/detail.html", context)


@login_required
def delete(request, pk):
    trade = get_object_or_404(Trades, pk=pk)
    if request.user == trade.user:
        trade.delete()
    return redirect("trade:index")


@login_required
def trade_comment(request, pk):
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
            comment_list.append(
                {
                    "user": c.user.username,
                    "content": c.content,
                    "create_at": c.create_at,
                    "pk": c.user.pk,
                    "comment_pk": c.pk,
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
            comment_list.append(
                {
                    "user": c.user.username,
                    "content": c.content,
                    "create_at": c.create_at,
                    "pk": c.user.pk,
                    "comment_pk": c.pk,
                }
            )
        context = {
            "comment_list": comment_list,
            "user": user.pk,
        }
    return JsonResponse(context)


def keyboard_search(request):
    form = CreateTrade()
    search_data = request.GET.get("search", "")
    keyboard = Trades.objects.filter(title__icontains=search_data)
    print(1)
    keyboard_list = []
    print(keyboard)
    for k in keyboard:
        keyboard_list.append(
            {
                "title": k.title,
            }
        )
    context = {
        "keyboard_list": keyboard_list,
    }
    return JsonResponse(context)
