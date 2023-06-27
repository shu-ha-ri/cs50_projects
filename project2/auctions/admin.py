from django.contrib import admin

# Register your models here.
from .models import AuctionListing, Bid, AutionListingComment

# only listings, bids and comments as asked in specification
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(AutionListingComment)