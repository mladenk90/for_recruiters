from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import Song, User, Category



def index(request):
    # query to get all songs and categories
    all_songs = Song.objects.filter(existing=True).order_by("id").reverse()
    Categories = Category.objects.all()
    #paginator
    paginator = Paginator(all_songs, 1)
    page_number = request.GET.get('page')
    page_songs = paginator.get_page(page_number)
    
    return render(request, "capstone/index.html", {
        "all_songs": all_songs,
        "page_songs": page_songs,
        "categories": Categories,
    })
    


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
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


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
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")

def view_category(request):
    # confirm POST request works
    if request.method == "POST":
        # get category selection from user
        categoryFromForm = request.POST['category']
        # ensure category selected is output
        category = Category.objects.get(category_name=categoryFromForm)
        # query to ensure song not already existing
        existing_songs = Song.objects.filter(existing=True, category=category)
        # Query for all items stored in the database
        Categories = Category.objects.all()
        # render affiliated html
        return render(request, "capstone/index.html", {
            # render corresponding songs
            "songs": existing_songs,
            # render corresponding categories
            "categories": Categories,
        })

# define create add song function
def add_song(request):
    # confirm GET request works
    if request.method == "GET":
        # Query for all items stored in the database
        Categories = Category.objects.all()
        # render affiliated html
        return render(request, "capstone/addsong.html", {
            # render corresponding categories
            "categories": Categories,
        })
    else:
        # submit data for title, artist name, image link, audio file, and category via POST method
        title = request.POST["title"]
        artist = request.POST["artist"]
        image = request.POST["image"]
        audio = request.POST["audio"]
        category = request.POST["category"]
        
        # query to get all content from Category model
        categoryData = Category.objects.get(category_name=category)
        # submit data for new song
        new_song = Song(
            title=title,
            image=image,
            category=categoryData,
            artist=artist,
            audio=audio,
            
        )
        #SAVE
        new_song.save()
        return HttpResponseRedirect(reverse(index))



# define function to view songs
def song(request, id):
    # get data from songs
    
    songData = Song.objects.get(pk=id)
    # confirm if already liked
    is_liked = request.user in songData.liked.all()
    
    # return same page with new button for like/unlike and add/remove to liked songs
    
    return render(request, "capstone/song.html", {
        "song": songData,
        "is_liked": is_liked,
        
        
    })


# define funtion for liked songs
def liked_songs(request):
    # confirm current user logged in
    current_user = request.user
    # confirm which songs in db are liked
    songs = current_user.liked.all()
    #paginator
    paginator = Paginator(songs, 1)
    page_number = request.GET.get('page')
    page_songs = paginator.get_page(page_number)
    return render (request, "capstone/likedsongs.html", {
        "songs": songs,
        "page_songs": page_songs,
    })
# define function for unlike button 
def unlike_song(request, id):
    # get data from songs
    songData = Song.objects.get(pk=id)
    # confirm current user logged in
    current_user = request.user
    # if liked, remove from liked database
    songData.liked.remove(current_user)
    return HttpResponseRedirect(reverse("song", args=(id, )))
# define function for like button 
def like_song(request, id):
    # get data from songs
    songData = Song.objects.get(pk=id)
    # confirm current user logged in
    current_user = request.user
    # if unliked, add to liked database
    songData.liked.add(current_user)
    return HttpResponseRedirect(reverse("song", args=(id, )))

