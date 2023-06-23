from django.urls import path

from . import views

# added URLs for entry lookup, search, create/edit entries and the random entry feature.
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:search_string>", views.show_entry, name="show_entry"),
    path("search", views.search_entries, name="search_entries"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("random_entry", views.random_entry, name="random_entry"),
    path("edit_entry/<str:title>", views.edit_entry, name="edit_entry"),
]
