from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from .models import Visit, Keyboard
from reviews.models import Review
from accounts.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.db.models import Count


def main(request):
    for i in Keyboard.objects.all():
        i.weight = (
            i.weight.replace("g", "")
            .replace("기타", "0")
            .replace("828.8", "828")
            .replace("506.4", "506")
            .replace("664.8", "664")
        )
        i.weight = int(i.weight)
        i.save()
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        upress = user.press
        uweight = user.weight
        usound = user.sound
        uconnect = user.connect
        uarray = user.array
        # print(uarray, uarray[0])
        press = [[] for _ in range(3)]
        weight = [[] for _ in range(2)]
        sound = [[] for _ in range(3)]
        connect = [[] for _ in range(3)]
        array = [[] for _ in range(3)]
        k = Keyboard.objects.all()
        ans1 = set()
        ans2 = set()
        ans3 = set()
        ans4 = set()
        ans5 = set()
        for i in k:
            press[2].append(i)
            weight[1].append(i)
            sound[2].append(i)
            connect[2].append(i)
            array[2].append(i)
            if i.press <= 45:
                press[0].append(i)
            else:
                press[1].append(i)
            if int(i.weight) <= 900:
                weight[0].append(i)
            if "저소음" in i.key_switch or ("Topre" in i.switch and "무접점" in i.connect):
                sound[1].append(i)
            else:
                sound[0].append(i)
            if "풀배열" in i.kind:
                array[0].append(i)
            elif "텐키리스" in i.kind:
                array[1].append(i)
            if "유선" in i.bluetooth or "블루투스" in i.bluetooth:
                connect[0].append(i)
            if "무선" in i.bluetooth or "블루투스" in i.bluetooth:
                connect[1].append(i)
        upress = int(upress[0]) - 1
        uweight = int(uweight[0]) - 1
        usound = int(usound[0]) - 1
        uconnect = int(uconnect[0]) - 1
        uarray = int(uarray[0]) - 1
        for value in press[upress]:
            ans1.add(value)
        for value in weight[uweight]:
            ans2.add(value)
        for value in sound[usound]:
            ans3.add(value)
        for value in connect[uconnect]:
            ans4.add(value)
        for value in array[uarray]:
            ans5.add(value)
        k = ans1 & ans2 & ans3 & ans4 & ans5
        items = list(set(k))[:3]
        # print(items)
        # print(len(sound[0]), len(sound[1]), len(sound[2]))
        # print(len(array[0]), len(array[1]), len(array[2]))
        # print(len(weight[0]), len(weight[1]))
        # print(len(press[0]), len(press[1]), len(press[2]))
        # print(len(connect[0]), len(connect[1]), len(connect[2]))
    else:
        items = []
    if Visit.objects.order_by("-pk"):
        visit_sum = 0
        today_visit = Visit.objects.order_by("-pk")[0].visit_count
        all_visit = Visit.objects.all()
        for i in all_visit:
            visit_sum += i.visit_count
        context = {"all": visit_sum, "today": today_visit, "items": items}
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
        context = {"items": items}
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


import random


def scroll_data(request):
    # 랜덤 광고
    ads = [
        {
            "name": "VARMILO MIYA PRO SEA MELODY PBT 염료승화 영문 저소음적축",
            "image": "https://funkeys.co.kr/data/apms/background/var_new_02.jpg",
            "url": "https://funkeys.co.kr/shop/item.php?it_id=1651475779&ca_id=10",
        },
        {
            "name": "VARMILO X ZOMO 고양이 발바닥 ABS 키캡 샴냥",
            "image": "https://funkeys.co.kr/data/apms/background/var_new_04.jpg",
            "url": "https://funkeys.co.kr/shop/item.php?it_id=1619427450&ca_id=20",
        },
        {
            "name": "DUCKY ONE 3 TKL Matcha PBT 이중사출 한글 저소음적축",
            "image": "https://funkeys.co.kr/data/item/1650969348/DUCKYONE3TKLMatcha_F.MAIN.jpg",
            "url": "https://funkeys.co.kr/shop/item.php?it_id=1650969339&ca_id=70",
        },
        {
            "name": "DUCKY ONE 3 RGB Yellow PBT 이중사출 한글 저소음적축",
            "image": "https://funkeys.co.kr/data/item/1650968289/thumb-DUCKYONE3RGBYellow_F.MAIN_600x750.jpg",
            "url": "https://funkeys.co.kr/shop/item.php?it_id=1650968289&ca_id=70",
        },
        {
            "name": "DUCKY ABS 심리스 이중사출 영문 SA 키캡 세트 Cotton candy",
            "image": "https://funkeys.co.kr/data/item/1629170024/thumb-04COTTONCANDY_600x750.png",
            "url": "https://funkeys.co.kr/shop/item.php?it_id=1629170024&ca_id=20",
        },
        {
            "name": "Intellilabs 노트북도 맞춤의 시대",
            "image": "/static/images/인텔리랩스.png",
            "url": "http://intellilabs-env.eba-cynacmth.ap-northeast-2.elasticbeanstalk.com/",
        },
        {
            "name": "Intellilabs 노트북도 맞춤의 시대",
            "image": "/static/images/인텔리랩스2.png",
            "url": "http://intellilabs-env.eba-cynacmth.ap-northeast-2.elasticbeanstalk.com/",
        },
    ]
    # 랜덤 개수
    random_ads = [random.choice(ads)]
    random2 = random.choice(ads)
    while random2 in random_ads:
        random2 = random.choice(ads)
    random_ads.append(random2)

    all_keyboard = Keyboard.objects.all()

    brand = request.GET.get("brand")
    key = request.GET.get("key")
    bluetooth = request.GET.get("bluetooth")
    data_press = request.GET.get("press")
    kind = request.GET.get("kind")
    page = request.GET.get("page")
    # 추가된 부분 111~112
    name = request.GET.get("name")

    q = Q()
    # 추가된 부분 115~116
    if name != "0":
        q &= Q(name__icontains=name)

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

    paginator = Paginator(keyboard_list, 32)
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
            "random_ads": random_ads,
        }

        return JsonResponse(context)

    except EmptyPage:
        context = {}
        return JsonResponse(context)


def detail(request, pk):
    keyboard = Keyboard.objects.get(pk=pk)
    reviews = Review.objects.filter(keyboard_id=pk)
    bests = (
        Review.objects.filter(keyboard_id=pk)
        .annotate(num_=Count("like_users"))
        .order_by("-num_")
    )
    aval = 0.0
    for review in reviews:
        aval += review.grade
    if aval > 0:
        aval /= len(reviews)
        aval = round(aval, 1)
    context = {
        "keyboard": keyboard,
        "aval": aval,
        "review": pk,
        "bests": bests,
    }
    return render(request, "articles/detail.html", context)
