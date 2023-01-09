from django.urls import path

from . import views

urlpatterns = [
    # path for index
    path("", views.index, name="index"),
    # path for entry/entries
    path("wiki/<str:title>", views.entry, name="entry"),
    # path for search
    path("search/", views.search, name="search"),
    # path for new page
    path("newpage/", views.new_page, name="new_page"),
    # path for random page
    path("randompage/", views.random_page, name="random_page"),
    # path for edit page
    path("editpage/", views.edit_page, name="edit_page"),
    # path to save edit page
    path("save/", views.save, name="save"),
]
