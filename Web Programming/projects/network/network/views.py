from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Following, Like

# function for index page
def index(request):
    # query to get all posts
    all_posts = Post.objects.all().order_by("id").reverse()
    
    #paginator
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    #query for liked by 
    liked_by = Like.objects.all()
    # query for liked
    liked = []
    try:
        for like in liked_by:
            if like.owner.id == request.owner.id:
                liked.append(like.post.id)
    except:
        liked = []
    # render html info for posts, pages, and likes
    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "page_posts": page_posts,
        "liked": liked,
    })

# function for profile page
def profile(request, user_id):
    # query to get user info and posts info
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(owner=user).order_by("id").reverse()
    # query to filter following users from followed users
    following = Following.objects.filter(owner_following=user)
    follower = Following.objects.filter(owner_follower=user)
    # confirm if user is already being followed
    try:
        check_following = follower.filter(user=User.objects.get(pk=request.user.id))
        if len(check_following) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False
    #paginator
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    # render html info for posts, pages, and likes for specific user profile
    return render(request, "network/profile.html", {
        "all_posts": all_posts,
        "page_posts": page_posts,
        "username": user.username,
        "following": following,
        "follower": follower,
        "is_following": is_following,
        "user_profile": user,
    })

# funtion to unlike
def unlike_post(request, post_id):
    # query to get post and user info
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    # query to filter user to specific post
    like = Like.objects.filter(owner=user, post=post)
    # DELETE post
    like.delete()
    # render message response via JS
    return JsonResponse({"message": "Unliked!"})

def like_post(request, post_id):
    # query to get post and user info
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    # query to filter user to specific post
    like = Like(owner=user, post=post)
    # SAVE
    like.save()
    # render message response via JS
    return JsonResponse({"message": "Liked!"})

# function to edit a post
def edit_post(request, post_id):
    # confirm POST method is used
    if request.method == "POST":
        # query to get current data of post
        data = json.loads(request.body)
        # query to specify post to edit
        edit = Post.objects.get(pk=post_id)
        # update initial data to updated data
        edit.content = data["content"]
        # SAVE
        edit.save()
        # render message response via JS
        return JsonResponse({"message": "Successfully Edited", "data": data["content"]})

def following_page(request):
    # query to confirm current user, follower, and all posts in question
    current_user = User.objects.get(pk=request.user.id)
    following_user = Following.objects.filter(owner_following=current_user)
    all_posts = Post.objects.all().order_by('id').reverse()
    # dict for posts following
    following_post = []
    # confirm who is user and post affiliation then add 
    for post in all_posts:
        for user in following_user:
            if user.owner_follower == post.owner:
                following_post.append(post)

    #paginator
    paginator = Paginator(following_post, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    # render html for pages
    return render(request, "network/following.html", {
        "page_posts": page_posts,
    })
# function for follow
def follow(request):
    # confirm followerr
    follow_user = request.POST['userfollow']
    # confirm current user
    current_user = User.objects.get(pk=request.user.id)
    # confirm user data
    user_data = User.objects.get(username=follow_user)
    # follow
    f = Following(owner_follower=current_user, owner_following=user_data)
    # SAVE
    f.save()
    # confirm user id
    user_id = user_data.id
    # render profile for corresponding user id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))
# function for unfollow
def unfollow(request):
    # confirm follower
    follow_user = request.POST['userfollow']
    # confirm current user
    current_user = User.objects.get(pk=request.user.id)
    # confirm user data
    user_data = User.objects.get(username=follow_user)
    # unfollow
    f = Following.objects.get(owner_follower=current_user, owner_following=user_data)
    # DELETE
    f.delete()
    # confirm user id
    user_id = user_data.id
    # render profile for corresponding user id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

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
# function for new post
def new_post(request):
    # confirm POST method is used
    if request.method == "POST":
        # query for content in new post
        content = request.POST['content']
        # confirm user who is posting
        user = User.objects.get(pk=request.user.id)
        # confirm user matches with post
        post = Post(content=content, owner=user)
        # post and SAVE
        post.save()
        # render html back to homepage
        return HttpResponseRedirect(reverse("index"))