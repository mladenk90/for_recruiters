from django.contrib import admin

from .models import Song, User, Category

# Register your models here.
admin.site.register(User)
admin.site.register(Song)
admin.site.register(Category)
