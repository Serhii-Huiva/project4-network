
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>", views.userPage, name="userPage"),
    path("<int:user_id>/following", views.following, name="following"),
    path("<int:user_id>/follow", views.follow, name="follow"),
    path("<int:post_id>/changepost", views.changePost, name="changePost"),
    path("<int:post_id>/likepost", views.likePost, name="likePost"),
    path("getlike", views.getLike, name="getLike")
]