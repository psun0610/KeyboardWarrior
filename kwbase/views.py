from django.shortcuts import render
from articles.models import Visit
from accounts.models import Notification

# Create your views here.
def base(request):
    today_visit = Visit.objects.order_by("-pk")[0].visit_count
    all_visit = Visit.objects.all()
    new_message = Notification.objects.filter(check=True)
    print(new_message, "gg")
    # count_message = len(new_message)
    c = 1
    print(c)
    context = {
        "today": today_visit,
        "all": all_visit,
        "c": c,
    }
    return render(request, "kwbase/base.html", context)
