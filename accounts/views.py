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
    'datas' : get_user_model().objects.all(),
    'user' : request.user,
  }
  return render(request, 'accounts/index.html', context)
def signup(request):
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            my_login(request, user)
            return redirect("articles:main")
    else:
        form = CreateUser()
    context = {
        "form": form,
    }
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
    user = get_user_model().objects.get(pk = pk)
    rank_percent = (user.rank % 1000) * 10
    context = {
    'user': user,
    'rank_percent' : rank_percent,
    }
    return render(request, 'accounts/detail.html', context)
#프로필 수정
@login_required
def edit_profile(request,pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
      if request.method == 'POST':
          form = CustomUserChangeForm(request.POST ,instance=request.user)
          if form.is_valid():
              user = form.save()  
              try:
                user.profile_image =request.FILES['image']
                user.save()
              except:
                print('error')
              return redirect('accounts:detail', user.pk)
      else:
          form = CustomUserChangeForm(instance=request.user)
      context = {
          'form': form,
      }
      return render(request,'accounts/edit_profile.html',context)
    else:
      return render(request,'articles/index.html')
@login_required
def change_password(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
      if request.method == 'POST':
          form = PasswordChangeForm(request.user, request.POST)
          if form.is_valid():
              user = form.save()
              update_session_auth_hash(request, user)  # Important!
              messages.success(request, 'Your password was successfully updated!')
              return redirect('accounts:edit_profile', user.pk)
          else:
              messages.error(request, 'Please correct the error below.')
      else:
          form = PasswordChangeForm(request.user)

      context = {
        'form': form,
      }
      
      return render(request, 'accounts/change_password.html',context)
    else:
      return render(request,'accounts/index.html')

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
        'isFollowing': is_following,
        'followers': user.followers.all().count(),
        'followings': user.followings.all().count(),
        }
    return JsonResponse(data)
