
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.create_post, name="create_post"),
    path("posts/<int:post_id>", views.posts, name="posts"),
    path("posts/<int:post_id>/likes", views.likes, name="likes"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("users/<int:user_id>", views.show_user, name="show_user"),
    path("users/<int:user_id>/followers", views.create_follower, name="create_follower"),

    path("show_following", views.show_following, name="show_following"),

    

]
