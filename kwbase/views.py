from django.shortcuts import render
from articles.models import Visit

# Create your views here.
def base(request):
    today_visit = Visit.objects.order_by("-pk")[0].visit_count
    all_visit = Visit.objects.all()
    context = {
        "today": today_visit,
        "all": all_visit,
    }
    return render(request, "kwbase/base.html", context)
