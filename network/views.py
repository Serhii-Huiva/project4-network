from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt


import datetime
import json

from .models import User, Post, Follow, Like


def index(request):
    if request.method == "GET":
        pageNum = request.GET.get('page')
        posts = Post.objects.all().order_by('-time')
        paginator = Paginator(posts, 10)
        pageResp = paginator.get_page(pageNum)

        return render(request, "network/index.html", {
            "posts": pageResp
        })
    else:
        now = datetime.datetime.now()
        user = request.user
        content = request.POST["newPost"]

        np = Post(user=user, content=content, time=now)
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
    pageNum = request.GET.get('page')

    user = User.objects.get(id = user_id)
    posts = Post.objects.all().filter(user=user).order_by('-time')

    paginator = Paginator(posts, 10)
    pageResp = paginator.get_page(pageNum)

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
        "posts": pageResp
    })

def following(request, user_id):
    pageNum = request.GET.get('page')

    user = User.objects.get(id = user_id)
    follows = Follow.objects.all().filter(user = user)

    if len(follows) > 0:
        notFollowing = False
        for f in range(len(follows)):
            userN = User.objects.get(username = follows[f].following)
            if f == 0:
                p0sts = Post.objects.all().filter(user = userN.id)
            else:
                p0sts = p0sts | Post.objects.all().filter(user = userN.id)

        posts = p0sts.order_by('-time')
    else:
        notFollowing = True
        posts = []

    paginator = Paginator(posts, 10)
    pageResp = paginator.get_page(pageNum)

    return render(request, "network/following.html", {
        "notFollowing": notFollowing,
        "posts": pageResp
    })

def followers(request, user_id):
    pageNum = request.GET.get('page')

    user = User.objects.get(id = user_id)
    followers = Follow.objects.all().filter(user = user)
    paginator = Paginator(followers, 10)
    pageResp = paginator.get_page(pageNum)

    print(pageResp)

    return render(request, "network/follow.html", {
        "username": user,
        "users": pageResp
    })

def follows(request, user_id):
    pageNum = request.GET.get('page')

    user = User.objects.get(id = user_id)
    follows = Follow.objects.all().filter(following = user)
    paginator = Paginator(follows, 10)
    pageResp = paginator.get_page(pageNum)

    return render(request, "network/follow.html", {
        "username": user,
        "users": pageResp
    })

@csrf_exempt
def follow(request, user_id):
    if request.method == "POST":
        req = json.loads(request.body)

        if req['follow']:
            newF = Follow(user=req['userName'], following=req['followUser'])
            newF.save()
        else:
            delF = Follow.objects.get(user=req['userName'], following=req['followUser'])
            delF.delete()
    
        return JsonResponse({"status": True}, status=200)

    else:
        userN = User.objects.get(id = user_id)
        fol = Follow.objects.all().filter(following = userN.username)
        followers =[]

        for f in fol:
            followers.append(f.user)

        return  HttpResponse(json.dumps(followers))

@csrf_exempt
def changePost(request, post_id):
    if request.method == "POST":
        req = json.loads(request.body)

        post = Post.objects.get(id = post_id)
        post.content = req['content']
        post.save()

        return JsonResponse({"status": True}, status=200)

@csrf_exempt
def likePost(request, post_id):
    if request.method == "POST":
        req = json.loads(request.body)
        post = Post.objects.get(id=post_id)

        if req["like"]:
            newL = Like(user=req["user"], post=post)
            newL.save()
            print('save')
        else:
            delL = Like.objects.get(user=req["user"], post=post)
            delL.delete()
            print('delete')
        
        return JsonResponse({"status": True}, status=200)

@csrf_exempt
def getLike(request):
    req = json.loads(request.body)
    IDlist = req['IDlist']

    responseList = {}

    for ID in IDlist:
        likeList = Like.objects.all().filter(post=ID)
        userList = []

        if len(likeList) > 0:
            for obj in likeList:
                userList.append(obj.user)

        responseList[ID] = userList

    return HttpResponse(json.dumps(responseList))

@csrf_exempt
def getFollow(request):
    req = json.loads(request.body)
    IDlist = req['IDlist']

    responseList = {}

    for ID in IDlist:
        f = []
        user = User.objects.get(id = ID)

        fowers = len(Follow.objects.all().filter(user = user.username))
        f.append(fowers)

        fows = len(Follow.objects.all().filter(following = user.username))
        f.append(fows)

        responseList[ID] = f

    return HttpResponse(json.dumps(responseList))