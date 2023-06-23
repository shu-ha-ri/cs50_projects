from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
import sys


class User(AbstractUser):
    pass


class AuctionListingCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    # Inspired by Ruby on Rails; Timestamping
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class AuctionListing(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="active_listings",
        blank=False,
        null=False,
    )
    title = models.CharField(max_length=100, blank=False, null=False)
    initial_price = models.FloatField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    category = models.ForeignKey(
        AuctionListingCategory,
        on_delete=models.CASCADE,
        related_name="auction_listings",
        blank=True,
        null=True,
    )
    image = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(blank=False, null=False)
    # Inspired by Ruby on Rails; Timestamping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_current_price(self):
        higest_bid = Bid.objects.filter(
            auction_listing=self).aggregate(Max('bid_price'))
        if higest_bid['bid_price__max']:
            return higest_bid['bid_price__max']
        else:
            return self.initial_price
        
    def get_bid_count(self):
        return len(Bid.objects.filter(auction_listing=self).all())
        
    def get_highest_bid_user(self):
        higest_bid = Bid.objects.filter(auction_listing=self).order_by('-bid_price')[0]
        return higest_bid.user
        
    def is_on_user_watchlist(self, user):
        watchlist_item = WatchlistItem.objects.filter(
            user = user,
            auction_listing = self,
            active = True
        ).first()
        return True if watchlist_item else False
        

class AutionListingComment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    auction_listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.CharField(max_length=255)
    # Inspired by Ruby on Rails; Timestamping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        # return super().__str__()
        return f"{self.author}: {self.comment}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids"
    )
    auction_listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="bids"
    )
    bid_price = models.FloatField(blank=False, null=False)
    # Inspired by Ruby on Rails; Timestamping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WatchlistItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auction_listing",
        blank=False,
        null=False,
    )
    auction_listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="watching_user"
    )
    active = models.BooleanField(blank=True, null=True)
    # Inspired by Ruby on Rails; Timestamping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def return_auction_listings(user):
        auction_listings = []
        watchlist_items = WatchlistItem.objects.filter(user=user, active=True).all()
        for item in watchlist_items:
            auction_listings.append(item.auction_listing)
        return auction_listings