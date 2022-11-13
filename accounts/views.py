import requests
from django.shortcuts import render, redirect
from .forms import CreateUser
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login as my_login, logout as my_logout
from django.contrib import messages
from .forms import CustomUserChangeForm

# Create your views here.


def index(request):
    context = {
        "datas": get_user_model().objects.all(),
        "user": request.user,
    }
    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CreateUser(request.POST)
        print(1)
        if form.is_valid():
            user = form.save()
            my_login(request, user)
            print(2)
            return redirect("articles:main")
    else:
        form = CreateUser()
        print(3)
    context = {
        "form": form,
    }
    print(form.errors)
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            my_login(request, form.get_user())
            messages.success(request, f"환영합니다")
            return redirect(request.GET.get("next") or "articles:main")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    my_logout(request)
    return redirect("articles:main")


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    rank_percent = (user.rank % 1000) * 10
    context = {
        "user": user,
        "rank_percent": rank_percent,
    }
    return render(request, "accounts/detail.html", context)


# 프로필 수정
@login_required
def edit_profile(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                user = form.save()
                try:
                    user.profile_image = request.FILES["image"]
                    user.save()
                except:
                    print("error")
                return redirect("accounts:detail", user.pk)
        else:
            form = CustomUserChangeForm(instance=request.user)
        context = {
            "form": form,
        }
        return render(request, "accounts/edit_profile.html", context)
    else:
        return render(request, "articles/index.html")


@login_required
def change_password(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, "Your password was successfully updated!")
                return redirect("accounts:edit_profile", user.pk)
            else:
                messages.error(request, "Please correct the error below.")
        else:
            form = PasswordChangeForm(request.user)

        context = {
            "form": form,
        }

        return render(request, "accounts/change_password.html", context)
    else:
        return render(request, "accounts/index.html")


# follow
@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)

    if request.user != user:
        if request.user not in user.followers.all():
            user.followers.add(request.user)
            is_following = True
        else:
            user.followers.remove(request.user)
            is_following = False
    data = {
        "isFollowing": is_following,
        "followers": user.followers.all().count(),
        "followings": user.followings.all().count(),
    }
    return JsonResponse(data)


import secrets

state_token = secrets.token_urlsafe(16)


def naver_request(request):
    naver_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
    client_id = "sr5Wb8p3_r8B_3nV9wKv"  # 배포시 보안적용 해야함
    redirect_uri = "http://localhost:8000/accounts/naver/login/callback/"
    state_token = secrets.token_urlsafe(16)
    return redirect(
        f"{naver_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state_token}"
    )


def naver_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "sr5Wb8p3_r8B_3nV9wKv",  # 배포시 보안적용 해야함
        "client_secret": "FtyMQDzlAQ",
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "redirect_uri": "http://localhost:8000/accounts/naver/login/callback/",
    }
    naver_token_request_url = "https://nid.naver.com/oauth2.0/token"
    access_token = requests.post(naver_token_request_url, data=data).json()[
        "access_token"
    ]

    headers = {"Authorization": f"bearer {access_token}"}
    naver_call_user_api = "https://openapi.naver.com/v1/nid/me"
    naver_user_information = requests.get(naver_call_user_api, headers=headers).json()

    naver_id = naver_user_information["response"]["id"]
    naver_nickname = naver_user_information["response"]["nickname"]

    if get_user_model().objects.filter(naver_id=naver_id).exists():
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    else:
        naver_login_user = get_user_model()()
        naver_login_user.username = naver_nickname
        naver_login_user.naver_id = naver_id
        naver_login_user.set_password(str(state_token))
        naver_login_user.save()
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    my_login(request, naver_user)
    return redirect(request.GET.get("next") or "articles:main")


def google_request(request):
    google_api = "https://accounts.google.com/o/oauth2/v2/auth"
    client_id = "598608554936-4rm80s1c7krbac2hs9f9f08vamnitvb7.apps.googleusercontent.com"  # 배포시 보안적용 해야함
    redirect_uri = "http://localhost:8000/accounts/login/google/callback/"
    google_base_url = "https://www.googleapis.com/auth"
    google_email = "/userinfo.email"
    google_myinfo = "/userinfo.profile"
    scope = f"{google_base_url}{google_email}+{google_base_url}{google_myinfo}"
    return redirect(
        f"{google_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )


def google_callback(request):
    data = {
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "grant_type": "authorization_code",
        "client_id": "598608554936-4rm80s1c7krbac2hs9f9f08vamnitvb7.apps.googleusercontent.com",  # 배포시 보안적용 해야함
        "client_secret": "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",
        "redirect_uri": "http://localhost:8000/accounts/login/google/callback/",
    }
    google_token_request_url = "https://oauth2.googleapis.com/token"
    access_token = requests.post(google_token_request_url, data=data).json()[
        "access_token"
    ]
    params = {
        "access_token": f"{access_token}",
    }
    google_call_user_api = "https://www.googleapis.com/oauth2/v3/userinfo"
    google_user_information = requests.get(google_call_user_api, params=params).json()

    google_id = google_user_information["sub"]
    google_name = google_user_information["name"]
    print(google_id)
    if get_user_model().objects.filter(goo_id=google_id).exists():
        google_user = get_user_model().objects.get(goo_id=google_id)
    else:
        google_login_user = get_user_model()()
        google_login_user.username = google_name
        google_login_user.goo_id = google_id
        google_login_user.set_password(str(state_token))
        google_login_user.save()
        google_user = get_user_model().objects.get(goo_id=google_id)
    my_login(request, google_user)
    return redirect(request.GET.get("next") or "articles:main")
