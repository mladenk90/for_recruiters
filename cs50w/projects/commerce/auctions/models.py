from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model

# define class for User
class User(AbstractUser):
    pass

#define class for Categories
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

#define class for bids
class Bid(models.Model):
    #confirm that bid field is number
    bid = models.IntegerField()
    # confirm owner and listing to match with bid
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

            
#define class for Listings
class Listing(models.Model):
    #confirm max lengths for titles, descriptions, and img urls
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=3000)
    #confirm that price field is float
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_offer")
    #confirm that not already existing
    existing = models.BooleanField(default=True)
    #update user database
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    #update category database
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    #allow watchlist to contain multiple listings
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    
    def __str__(self):
        return self.title
        


#define class for comments
class Comment(models.Model):
    # confirm owner and listing to match with comment
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment")
    # content of comment
    content = models.CharField(max_length=250, null=True)
    
    def __str__(self):
        return f"{self.owner} commented on {self.listing}"