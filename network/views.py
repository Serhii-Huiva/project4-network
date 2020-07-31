from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect #JsonResponse HttpResponse, 
from django.shortcuts import render, redirect
from django.urls import reverse
#from django.core.paginator import Paginator
# from django.utils import timezone

# from django.views.decorators.csrf import csrf_exempt


import datetime

from .models import User, Post, Follow


def index(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by('-time')
        return render(request, "network/index.html", {
            "posts": posts,
        })
    else:
        now = datetime.datetime.now()
        user = request.user
        content = request.POST["newPost"]

        np = Post(user=user, content=content, time=now, like=0)
        np.save()

        return redirect ("/")



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def userPage(request, user_id):
    user = User.objects.get(id = user_id)
    posts = Post.objects.all().filter(user=user).order_by('-time')
    try:
        followers = len(Follow.objects.all().filter(following = user))
        follows = len(Follow.objects.all().filter(user = user))
    except Follow.DoesNotExist:
        followers = 0
        follows = 0

    return render(request, "network/userpage.html", {
        "username": user,
        "followers": followers,
        "followed": follows,
        "posts": posts
    })

def following(request, user_id):
    user = User.objects.get(id = user_id)
    follows = Follow.objects.all().filter(user = user)

    if len(follows) > 0:
        notFollowing = False
        for foll in follows:
            p0sts = Post.objects.all().filter(user = foll.following)
        posts = p0sts.order_by('-time')
    else:
        notFollowing = True
        posts = []

    return render(request, "network/following.html", {
        "notFollowing": notFollowing,
        "posts": posts
    })