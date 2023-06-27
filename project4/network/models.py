from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def get_reverse_chronological_posts(self):
        return self.posts.all().order_by("-updated_at")
    
    def get_active_followers(self):
        return self.followers.filter(active=True)
    
    def get_active_following(self):
        return self.following.filter(active=True)
    

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    user_likes = models.ManyToManyField(User)

    def count_likes(self):
        return self.likes.filter(active=True).count()
    
    def serialize(self):
        return {
            "id": self.id,
            "user": {
                "user_id": self.user.id
            },
            "body": self.body,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "updated_at": self.updated_at.strftime("%b %d %Y, %I:%M %p")
        }



class Follower(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    active = models.BooleanField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    

class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    active = models.BooleanField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "post": {
                "post_id": self.post.id
            },
            "user": {
                "user_id": self.user.id
            },
            "active": self.active,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "updated_at": self.updated_at.strftime("%b %d %Y, %I:%M %p")
        }