from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Follower

# only listings, bids and comments as asked in specification
admin.site.register(Follower)