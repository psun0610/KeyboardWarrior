from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/edit_profile/", views.edit_profile, name="edit_profile"),
    path("<int:pk>/change_password/", views.change_password, name="change_password"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("login/naver/", views.naver_request, name="naver"),
    path("naver/login/callback/", views.naver_callback),
    path("login/google/", views.google_request, name="google"),
    path("login/google/callback/", views.google_callback),
    path("<int:pk>/social_form/", views.social_form, name="social_form"),
    path("<int:trade_pk>/<int:user_pk>/message/", views.message, name="message"),
    path(
        "<int:trade_pk>/<int:user_pk>/first_message/",
        views.first_message,
        name="first_message",
    ),
    path("messageCheck/", views.messageCheck, name="messageCheck"),
]
