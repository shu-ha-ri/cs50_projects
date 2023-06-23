from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("show_user/<int:user_id>", views.show_user, name="show_user"),

    path("listing/new", views.create_listing, name="create_listing"),
    path("listing/<int:auction_listing_id>", views.show_listing, name="show_listing"),
    path("listing/<int:auction_listing_id>/edit", views.edit_listing, name="edit_listing"),

    path("remove_from_watchlist/<int:auction_listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_to_watchlist/<int:auction_listing_id>", views.add_to_watchlist, name="add_to_watchlist"),


    path("create_bid", views.create_bid, name="create_bid"),

    path("close_auction/<int:auction_listing_id>", views.close_auction, name="close_auction"),

    path("create_comment", views.create_comment, name="create_comment"),

    path("show_watchlist", views.show_watchlist, name="show_watchlist"),

    path("show_categories", views.show_categories, name="show_categories"),
    path("category/<int:category_id>", views.show_category, name="show_category"),
    
    
]
