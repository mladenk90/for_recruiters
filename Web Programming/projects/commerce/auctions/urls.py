from django.urls import path

from . import views

urlpatterns = [
    # path for index
    path("", views.index, name="index"),
    # path for login
    path("login", views.login_view, name="login"),
    # path for logout
    path("logout", views.logout_view, name="logout"),
    # path for register
    path("register", views.register, name="register"),
    # path for create new listing
    path("createlisting", views.create_listing, name="create listing"),
    # path for viewing listings
    path("listing/<int:id>", views.listing, name="listing"),
    # path for watchlist
    path("watchlist", views.watchlist, name="watchlist"),
    # path for removing watchlist
    path("removewatchlist/<int:id>", views.remove_watchlist, name="remove from watchlist"),
    # path for removing watchlist
    path("addwatchlist/<int:id>", views.add_watchlist, name="add to watchlist"),
    # path for viewing category
    path("viewcategory", views.view_category, name="view category"),
    # path for adding comment
    path("addcomment/<int:id>", views.add_comment, name="add comment"),
    # path for adding bid
    path("bid/<int:id>", views.bid, name="add bid"),
    # path for adding bid
    path("close/<int:id>", views.close, name="close auction"),
]
