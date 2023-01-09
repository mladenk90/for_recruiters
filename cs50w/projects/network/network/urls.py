
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
    # path for new post
    path("newpost", views.new_post, name="new post"),
    # path for profile
    path("profile/<int:user_id>", views.profile, name="profile"),
    # path for follow
    path("follow", views.follow, name="follow"),
    # path for unfollow
    path("unfollow", views.unfollow, name="unfollow"),
    # path for following page
    path("following", views.following_page, name="following page"),
    # path for editing post
    path("edit/<int:post_id>", views.edit_post, name="edit post"),
    # path for like
    path("like/<int:post_id>", views.like_post, name="like"),
    # path for unlike
    path("unlike/<int:post_id>", views.unlike_post, name="unlike"),
]
