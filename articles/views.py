from django.shortcuts import render, redirect

from datetime import date, datetime, timedelta
from .models import Visit
from .models import Keyboard

def main(request):
    if Visit.objects.order_by("-pk"):
        visit_sum = 0
        today_visit = Visit.objects.order_by("-pk")[0].visit_count
        all_visit = Visit.objects.all()
        for i in all_visit:
            visit_sum += i.visit_count
        context = {
            "all":visit_sum,
            "today":today_visit
        }
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
            cookievalue += f"{request.user}"
            response.set_cookie("request.user", value=cookievalue, max_age=max_age, httponly=True)
            if not Visit.objects.all():
                Visit.objects.create(visit_date = str(now)[:10], visit_count = 1)
                print(str(now)[:10], 1)
            else:
                before = Visit.objects.order_by("-pk")[0]
                after = str(now)[:10]

                if before.visit_date != after:
                    Visit.objects.create(visit_date = str(now)[:10], visit_count = 1)
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
            cookievalue += f"{request.user}"
            response.set_cookie("request.user", value=cookievalue, max_age=max_age, httponly=True)
            if not Visit.objects.all():
                Visit.objects.create(visit_date = str(now)[:10], visit_count = 1)
                print(str(now)[:10], 1)
            else:
                before = Visit.objects.order_by("-pk")[0]
                after = str(now)[:10]

                if before.visit_date != after:
                    Visit.objects.create(visit_date = str(now)[:10], visit_count = 1)
                else:
                    before.visit_count += 1
                    before.save()
        return response
def all(request):
    return render(request, "articles/all.html")

def detail(request):
    
    li = [1,2,3]
    context = {
        'li' : li,
    }
    return render(request, "articles/detail.html", context)
