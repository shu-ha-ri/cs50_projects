from django.contrib import admin

# Register your models here.
from .models import AuctionListing, AuctionListingCategory, WatchlistItem, Bid, AutionListingComment

admin.site.register(AuctionListing)
admin.site.register(AuctionListingCategory)
admin.site.register(WatchlistItem)
admin.site.register(Bid)
admin.site.register(AutionListingComment)