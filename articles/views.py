from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from .models import Visit, Keyboard
from reviews.models import Review
from accounts.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q


def main(request):
    all_keyboard = Keyboard.objects.all()
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        press = user.press # 가벼움(45이하), 무거움(45초과), 상관없음
        weight = user.weight # 가벼움(900g이하), 상관없음(900초과)
        sound = user.sound #경쾌한소리, 조용한소리(저소음단어,무접점 토프레), 상관없음
        connect = user.connect # 유 무 상관없음
        array = user.array # ten = 풀배열 텐키리스=텐키리스 상관없음
    # for i in all_keyboard:
    #     print(i.key_switch)
    #     print(i.kind)
    #     print(i.bluetooth)
    #     print(i.press)
    #     print(i.weight)
    if Visit.objects.order_by("-pk"):
        visit_sum = 0
        today_visit = Visit.objects.order_by("-pk")[0].visit_count
        all_visit = Visit.objects.all()
        for i in all_visit:
            visit_sum += i.visit_count
        context = {"all": visit_sum, "today": today_visit}
        response = render(request, "articles/main.html", context)
        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(days=1)
        expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()

        cookievalue = request.COOKIES.get("request.user", "")
        if request.user == "AnonymousUser":
            cookievalue = request.COOKIES.get("sessionid", "")
        if f"{request.user}" not in cookievalue:
            cookievalue += f"{request.user.username.encode('utf8')}"
            response.set_cookie(
                "request.user", value=cookievalue, max_age=max_age, httponly=True
            )
            if not Visit.objects.all():
                Visit.objects.create(visit_date=str(now)[:10], visit_count=1)
                print(str(now)[:10], 1)
            else:
                before = Visit.objects.order_by("-pk")[0]
                after = str(now)[:10]

                if before.visit_date != after:
                    Visit.objects.create(visit_date=str(now)[:10], visit_count=1)
                else:
                    before.visit_count += 1
                    before.save()
        return response
    else:
        response = render(request, "articles/main.html")
        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(days=1)
        expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()

        cookievalue = request.COOKIES.get("request.user", "")
        if request.user == "AnonymousUser":
            cookievalue = request.COOKIES.get("sessionid", "")
        if f"{request.user}" not in cookievalue:
            cookievalue += f"{request.user.username.encode('utf8')}"
            response.set_cookie(
                "request.user", value=cookievalue, max_age=max_age, httponly=True
            )
            if not Visit.objects.all():
                Visit.objects.create(visit_date=str(now)[:10], visit_count=1)
                print(str(now)[:10], 1)
            else:
                before = Visit.objects.order_by("-pk")[0]
                after = str(now)[:10]

                if before.visit_date != after:
                    Visit.objects.create(visit_date=str(now)[:10], visit_count=1)
                else:
                    before.visit_count += 1
                    before.save()
        return response


def all(request):
    all_keyboard = Keyboard.objects.all()[:16]
    context = {
        "all_keyboard": all_keyboard,
    }
    return render(request, "articles/all.html", context)



def scroll_data(request):
    all_keyboard = Keyboard.objects.all()

    brand = request.GET.get("brand")
    key = request.GET.get("key")
    bluetooth = request.GET.get("bluetooth")
    data_press = request.GET.get("press")
    kind = request.GET.get("kind")
    page = request.GET.get("page")

    q = Q()
    if brand != "0":
        q &= Q(brand__icontains=brand)

    if key != "0":
        q &= Q(key_switch__icontains=key)

    if bluetooth != "0":
        q &= Q(bluetooth__icontains=bluetooth)

    if data_press != "0":
        if data_press == "1":
            press = []
            for num in range(1, 40):
                press.append(num)
            q &= Q(press__in=press)

        elif data_press == "2":
            press = []
            for num in range(40, 50):
                press.append(num)
            q &= Q(press__in=press)

        elif data_press == "3":
            press = []
            for num in range(50, 101):
                press.append(num)
            q &= Q(press__in=press)

    if kind != "0":
        q &= Q(kind__icontains=kind)
    keyboard_list = Keyboard.objects.filter(q)

    paginator = Paginator(keyboard_list, 8)
    try:
        page_obj = paginator.page(page)
        keyboards = []
        for k in page_obj:
            keyboards.append(
                {
                    "name": k.name,
                    "img": k.img,
                    "brand": k.brand,
                    "content": k.connect,
                    "array": k.array,
                    "switch": k.switch,
                    "key_switch": k.key_switch,
                    "press": k.press,
                    "weight": k.weight,
                    "kind": k.kind,
                    "pk": k.pk,
                }
            )

        context = {
            "keyboards": keyboards,
        }

        return JsonResponse(context)

    except EmptyPage:
        context = {}
        return JsonResponse(context)


def detail(request, pk):
    keyboard = Keyboard.objects.get(pk=pk)
    reviews = Review.objects.filter(keyboard_id = pk)
    aval = 0.0
    for review in reviews:
        aval += review.grade
    if aval > 0:
        aval /= len(reviews)
        aval = round(aval, 1)
    context = {
        "keyboard": keyboard,
        "aval": aval,
        "review":pk,
    }
    return render(request, "articles/detail.html", context)
