from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


# class for user info
class User(AbstractUser):
    pass

#define class for Categories
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

# class for songs
class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=50)
    image = models.CharField(max_length=500)
    
    audio = models.FileField(blank=True, null = True)
    #confirm that not already existing
    existing = models.BooleanField(default=True)
    #update user database
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    #update category database
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    #allow liked to contain multiple songs
    liked = models.ManyToManyField(User, blank=True, null=True, related_name="liked")
    paginate_by = 2
    
    def __str__(self):
        return self.title