from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment


def index(request):
    # query to ensure listing not already existing
    active_listings = Listing.objects.filter(existing=True)
    # Query for all items stored in the database
    Categories = Category.objects.all()
    # render affiliated html
    return render(request, "auctions/index.html", {
        # render corresponding listings
        "listings": active_listings,
        # render corresponding categories
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
        
# define function to view specific category
def view_category(request):
    # confirm POST request works
    if request.method == "POST":
        # get category selection from user
        categoryFromForm = request.POST['category']
        # ensure category selected is output
        category = Category.objects.get(category_name=categoryFromForm)
        # query to ensure listing not already existing
        active_listings = Listing.objects.filter(existing=True, category=category)
        # Query for all items stored in the database
        Categories = Category.objects.all()
        # render affiliated html
        return render(request, "auctions/index.html", {
            # render corresponding listings
            "listings": active_listings,
            # render corresponding categories
            "categories": Categories,
        })

# define create new listing function
def create_listing(request):
    # confirm GET request works
    if request.method == "GET":
        # Query for all items stored in the database
        Categories = Category.objects.all()
        # render affiliated html
        return render(request, "auctions/createlisting.html", {
            # render corresponding categories
            "categories": Categories
        })
    else:
        # submit data for title, description, image link, price, and category via POST method
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]
        # confirm user
        current_user = request.user
        # query to get all content from Category model
        categoryData = Category.objects.get(category_name=category)
        # create a bid
        bid = Bid(bid=int(price), owner=current_user)
        bid.save()
        # submit data for new listing
        new_listing = Listing(
            title=title,
            description=description,
            image=image,
            # ensure price can be a float
            price=bid,
            category=categoryData,
            owner=current_user
        )
        #save listing in database and redirect to homepage/active listings
        new_listing.save()
        return HttpResponseRedirect(reverse(index))



# define function to view listings
def listing(request, id):
    # get data from listings
    listingData = Listing.objects.get(pk=id)
    # query to confirm if already in watchlist
    in_watchlist = request.user in listingData.watchlist.all()
    # query to get comment for specific listing
    all_comments = Comment.objects.filter(listing=listingData)
    # return same page with new button for add/remove and add/remove to watchlist
    current_user = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "in_watchlist": in_watchlist,
        "all_comments": all_comments,
        "current_user": current_user,
    })

# define function for watchlist
def watchlist(request):
    # confirm current user
    current_user = request.user
    # obtain all data from watchlist
    listings = current_user.watchlist.all()
    #render watchlist html
    return render (request, "auctions/watchlist.html", {
        "listings": listings,
    }) 

# define function for removing from watchlist
def remove_watchlist(request, id):
    # get data from listings
    listingData = Listing.objects.get(pk=id)
    # confirm current user
    current_user = request.user
    # remove current users currently added listings
    listingData.watchlist.remove(current_user)
    # return same page with new button for add
    return HttpResponseRedirect(reverse("listing", args=(id, )))

# define function for adding to watchlist
def add_watchlist(request, id):
    # get data from listings
    listingData = Listing.objects.get(pk=id)
    # confirm current user
    current_user = request.user
    # add current users not currently added listings
    listingData.watchlist.add(current_user)
    # return same page with new button for remove
    return HttpResponseRedirect(reverse("listing", args=(id, )))

# define function to add comments
def add_comment(request, id):
    # confirm current user
    current_user = request.user
    # get data from listings
    listingData = Listing.objects.get(pk=id)
    # confirm POST method on comments
    content = request.POST['comment']
    # obtain owner,listing,content from models
    comment = Comment(
        owner=current_user,
        listing=listingData,
        content=content
    )
    # SAVE!!!
    comment.save()
    # return same page with new comment added
    return HttpResponseRedirect(reverse("listing", args=(id, )))

# define function to add bids
def bid(request, id):
    # confirm POST method on bid
    bid_offer = request.POST['bid_offer']
    # confirm current user
    current_user = request.user
    # query to get all listing data with pk's
    listingData = Listing.objects.get(pk=id)
    # confirm bid is greater than initial offer
    if int(bid_offer) > listingData.price.bid:
        # update bid in database with user info
        update_bid = Bid(owner=current_user, bid=int(bid_offer))
        # SAVE
        update_bid.save()
        # return to listing page with 'success' popup
        return render(request, "auctions/listing.html", {
        "listing": listingData,
        "content": "Successful Bid. Congratulations!",
        "updated": True,
        })
    else:
        # return to listing page with 'failure' popup
        return render(request, "auctions/listing.html", {
        "listing": listingData,
        "content": "Failed Bid/Invalid Amount. Please Post a Bid Higher than the Active Bid and Try Again!",
        "updated": False,
        })

# define function to close bid as owner of listing
def close(request, id):
    # query to get all listing data with pk's
    listingData = Listing.objects.get(pk=id)
    # ensure not in active listings
    listingData.active_listings = False
    # SAVE
    listingData.save()
    # confirm you are the owner of listing to close
    current_user = request.user.username == listingData.owner.username
    # if in watchlist, update db
    in_watchlist = request.user in listingData.watchlist.all()
    # if comments, update db
    all_comments = Comment.objects.filter(listing=listingData)
    # return to listing page with 'success' popup
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "in_watchlist": in_watchlist,
        "all_comments": all_comments,
        "current_user": current_user,
        "updated": True,
        "content": "Successfully Closed this Auction. Congatulations!"
    })