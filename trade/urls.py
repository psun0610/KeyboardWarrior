from django.urls import path, include
from . import views


app_name = "trade"


urlpatterns = [
    path("index/", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/comment/", views.trade_comment, name="comment"),
    path(
        "<int:trade_pk>/<int:comment_pk>/comment_delete/",
        views.delete_comment,
        name="comment_delete",
    ),
    path("keyboard_search/", views.keyboard_search, name="keyboard_search"),
    path("<int:pk>/marker/", views.marker, name="marker"),
    path("trade_search/", views.trade_search, name="trade_search"),
    path("<int:pk>/send_market", views.send_market, name="send_market"),
    path("<int:pk>/status/", views.status, name="status"),
]
