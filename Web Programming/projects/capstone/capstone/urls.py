from django.urls import path

from . import views

urlpatterns = [
    # path for homepage
    path("", views.index, name="index"),
    # path for login
    path("login", views.login_view, name="login"),
    # path for logout
    path("logout", views.logout_view, name="logout"),
    # path for register
    path("register", views.register, name="register"),
    # path for add new song
    path("addsong", views.add_song, name="add song"),
    # path for viewing songs
    path("song/<int:id>", views.song, name="song"),
    # path for liked songs
    path("likedsongs", views.liked_songs, name="liked songs"),
    # path for adding liked song
    path("likesong/<int:id>", views.like_song, name="like song"),
    # path for removing liked song
    path("unlikesong/<int:id>", views.unlike_song, name="unlike song"),
    # path for viewing category
    path("viewcategory", views.view_category, name="view category"),
]