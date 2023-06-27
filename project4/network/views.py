from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from .models import User, Post, Follower, Like

def index(request):
    posts = Post.objects.all().order_by("-updated_at")
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", 
                  {'page_obj': page_obj, 'user': request.user })


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
            return render(request, "network/login.html", 
                          {"message": "Invalid username and/or password."})
    else:
        return render(request, "network/login.html")


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def create_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        post = Post(
            user = request.user,
            body = request.POST["body"]
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        response = HttpResponse('400 Bad Request.')
        response.status_code = 400
        return response


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


def show_user(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "GET":
        profile_user = User.objects.get(pk=user_id)
        currently_following = profile_user.followers.filter(
            user=profile_user,
            follower=request.user,
            active=True).count() > 0
        return render(request, "network/show_user.html", { 
            "profile_user": profile_user,
             "currently_following": currently_following
            })
    else:
        response = HttpResponse('400 Bad Request.')
        response.status_code = 400
        return response


def create_follower(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        profile_user = User.objects.get(pk=user_id)
        if profile_user:
            follower = Follower.objects.filter(
                user=profile_user, 
                follower=request.user)
            if follower:
                if follower[0].active == True:
                    # Already follwing, unfollow/deactivate
                    follower[0].active = False
                else:
                    # Already follwing but inactive, reactivate
                    follower[0].active = True
                follower[0].save()
            else:
                # Not yet following, create and activate
                follower = Follower(
                    user=profile_user, 
                    follower=request.user,
                    active=True)
                follower.save()
            return HttpResponseRedirect(reverse("show_user", args=(user_id,)))
        else:
            response = HttpResponse('404 Resource Not Found.')
        response.status_code = 404
        return response
    else:
        response = HttpResponse('400 Bad Request.')
        response.status_code = 400
        return response
    


def show_following(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    following_user_ids = Follower.objects.filter(
        follower=request.user,
        active=True
    ).values_list('user_id', flat=True)
    posts = Post.objects.filter(user_id__in=following_user_ids).order_by("-updated_at")

    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/show_following.html", {
        "page_obj": page_obj
    })
        


def posts(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "PUT":
        # Edit post
        post = Post.objects.get(pk=post_id)
        if request.user == post.user:
            data = json.loads(request.body)
            post.body = data.get("postBody")
            post.save()
            return JsonResponse(post.serialize(), safe=False)
        else:
            return JsonResponse({"error": "400 Bad Request."}, status=400)

    
def likes(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        like = Like.objects.filter(user=request.user, post_id=post_id)
        post = Post.objects.get(pk=post_id)
        if like:
            like = like.first()
            if like.active:
                like.active = False
                post.user_likes.remove(request.user)
                post.save()
            else:
                like.active = True
                post.user_likes.add(request.user)
        else:
            like = Like(
                user=request.user,
                post=post,
                active=True)
            post.user_likes.add(request.user)
        like.save()
        post.save()
        return JsonResponse(
            { "like": like.serialize(), "post_like_count": post.count_likes() }, 
            safe=False)
    else:
        return JsonResponse({"error": "400 Bad Request."}, status=400)