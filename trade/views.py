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
    comments = Trade_Comment.objects.all()
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


def trade_comment(request, pk):
    trade = get_object_or_404(Trades, pk=pk)
    if request.method == "POST":
        form = CreateComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.trade = trade
            comment.save()
        comments = Trade_Comment.objects.filter(trade=pk).order_by("-pk")
        context = {"comments": comments}
        return JsonResponse(context)
