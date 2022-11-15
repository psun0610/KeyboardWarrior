from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from .models import Visit, Keyboard
from reviews.models import Review
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q



def main(request):
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
    all_keyboard = Keyboard.objects.all()
    context = {
        "all_keyboard": all_keyboard,
    }
    return render(request, "articles/all.html", context)

def alll(request):
    # all_keyboard = Keyboard.objects.all()
    # all_date = [[] for _ in range(len(all_keyboard))]
    # for i in range(len(all_keyboard)):
    #     all_date[i].append(all_keyboard[i].brand)
    #     all_date[i].append(all_keyboard[i].key_switch)
    #     all_date[i].append(all_keyboard[i].connect)
    #     all_date[i].append(all_keyboard[i].press)
    #     all_date[i].append(all_keyboard[i].array)
    radio_list = ['brand', 'key-switch', 'bluetooth', 'press', 'array']
    brand = request.GET.get('brand')
    key_switch = request.GET.get('key')
    bluetooth = request.GET.get('bluetooth')
    press = request.GET.get('press')
    array = request.GET.get('array')
    context = {
        "brand": brand,
        "key_switch" : key_switch,
        "bluetooth" : bluetooth,
        "press" : press,
        "array" : array,
    }
    return JsonResponse(context)

def scroll_data(request):
    all_keyboard = Keyboard.objects.all()

    brand = request.GET.get("brand")
    key = request.GET.get("key")
    bluetooth = request.GET.get("bluetooth")
    press = request.GET.get("press")
    array = request.GET.get("array")
    page = request.GET.get("page")
    print(brand)
    print(key)
    print(bluetooth)
    all_date = [[] for _ in range(len(all_keyboard))]
    # for i in range(len(all_keyboard)):
    # all_date[i].append(all_keyboard[i].brand)
    # all_date[i].append(all_keyboard[i].key_switch)
    # all_date[i].append(all_keyboard[i].connect)
    # all_date[i].append(all_keyboard[i].press)
    # all_date[i].append(all_keyboard[i].array)
    radio_list = ["brand", "key_switch", "bluetooth", "press", "array"]
    q = Q()

    if brand != "0":
        q &= Q(brand__contains=brand)

    if key != "0":
        q &= Q(key_switch__contains=key)

    if bluetooth != "0":
        q &= Q(connect__contains=bluetooth)

    if press != "0":
        q &= Q(press__contains=press)

    if array != "0":
        q &= Q(array__icontains=array)
    print(q)
    keyboard_list = Keyboard.objects.filter(q)
    paginator = Paginator(keyboard_list, 16)
    page_obj = paginator.page(page)
    keyboards = []
    for k in keyboard_list:
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
    print(keyboards)
    context = {
        "keyboards": keyboards,
    }

    return JsonResponse(context)


def detail(request, pk):
    keyboard = Keyboard.objects.get(pk=pk)
    reviews = Review.objects.filter(keyboard_id = pk)
    aval = 0
    for review in reviews:
        aval += review.grade
    aval /= len(reviews)
    aval = round(aval,1)
    context = {
        "keyboard": keyboard,
        "aval": aval
    }
    return render(request, "articles/detail.html", context)
