from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import sys

from .models import (AuctionListing, User, AuctionListingCategory, 
                     WatchlistItem, Bid, AutionListingComment, AuctionListingCategory)

def index(request):
    auction_listings = AuctionListing.objects.all()
    return render(request, 'auctions/index.html', {
        'auction_listings': auction_listings
    })

def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'auctions/login.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'auctions/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'auctions/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/register.html')


@login_required
def show_user(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'auctions/show_user.html', {
        'user': user,
        'user_auctions': []
    })


@login_required
def create_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        initial_price = request.POST['initial_price']
        description = request.POST['description']
        category = AuctionListingCategory.objects.get(pk=request.POST['category']) 
        image = request.POST['image']

        # TODO: Validation!

        auction_listing = AuctionListing(
            user = request.user,
            title = title,
            initial_price = initial_price,
            description = description,
            category = category,
            image = image
        )
        auction_listing.save()
        return HttpResponseRedirect(reverse('show_listing', args=(auction_listing.id,)))

    if request.method == 'GET': 
        categories = AuctionListingCategory.objects.all()
        return render(request, 'auctions/create_listing.html', { 
            'auction_listing_categories': categories
         })


def show_listing(request, auction_listing_id):
    auction_listing = AuctionListing.objects.get(pk=auction_listing_id)
    return render(request, 'auctions/show_listing.html', { 
            'watchlist_item': auction_listing.is_on_user_watchlist(request.user),
            'auction_listing': auction_listing,
         })


@login_required
def remove_from_watchlist(request, auction_listing_id):
    """ 
    Opted for deactivation instead of deleting the db entry. This allows
    for analysis of user preference even after items were removed again.
    To prevent flooding with duplicates, we're checking before creation
    and reactivate it again if it was deavtivated before.
    """
    auction_listing = AuctionListing.objects.get(pk=auction_listing_id)
    watchlist_enty = WatchlistItem.objects.filter(
        user = request.user,
        auction_listing = auction_listing,
        active = True
    ).first()
    watchlist_enty.active = False
    watchlist_enty.save()
    return HttpResponseRedirect(reverse('show_listing', args=(auction_listing.id,)))


@login_required
def add_to_watchlist(request, auction_listing_id):
    auction_listing = AuctionListing.objects.get(pk=auction_listing_id)

    # Conditionals leave out  case of active entry, which could only come
    # by directly accessing URL. Can be ignored and item is kept on list.
    watchlist_enty = WatchlistItem.objects.filter(
        user = request.user,
        auction_listing = auction_listing,
        active = False
    ).first()
    if watchlist_enty:
        # Reactivate old entry
        watchlist_enty.active = True
    else:
        # Create new entry
        watchlist_enty = WatchlistItem(
            user = request.user,
            auction_listing = auction_listing,
            active = True
        )
    watchlist_enty.save()

    return HttpResponseRedirect(reverse('show_listing', args=(auction_listing.id,)))


@login_required
def create_bid(request):
    if request.method == "POST":
        auction_listing = AuctionListing.objects.get(pk=request.POST['auction_listing_id'])
        bid_price = float(request.POST['bid_price'])
        if auction_listing:
            if auction_listing.user != request.user:
                if bid_price >= auction_listing.initial_price and bid_price > auction_listing.get_current_price():
                    bid = Bid(
                        user = request.user,
                        auction_listing = auction_listing,
                        bid_price = bid_price
                    )
                    bid.save()
                    messages.add_message(request, messages.SUCCESS, f'Your bid of {bid_price} was the highest current bid and was successfully placed.')
                else:
                    messages.add_message(request, messages.ERROR, f'Your bid was not high enough. Please bid more than the current price.')
                
                return HttpResponseRedirect(reverse('show_listing', args=(auction_listing.id,)))
            else:
                response = HttpResponse('400 Bad Request.')
                response.status_code = 400
                return response
        else:
            response = HttpResponse('404 Resource Not Found')
            response.status_code = 404
            return response
        

@login_required
def close_auction(request, auction_listing_id):
    auction_listing = AuctionListing.objects.get(pk=auction_listing_id)
    if auction_listing:
        auction_listing.active = False
        auction_listing.save()
        return HttpResponseRedirect(reverse('show_listing', args=(auction_listing.id,)))
    else:
        response = HttpResponse('404 Resource Not Found')
        response.status_code = 404
        return response


@login_required
def create_comment(request):
    auction_listing = AuctionListing.objects.get(pk=request.POST['auction_listing_id'])
    if request.method == "POST":
        comment = AutionListingComment(
            author = request.user,
            auction_listing = auction_listing,
            comment = request.POST['comment']
        )
        comment.save()
        return HttpResponseRedirect(reverse('show_listing', args=(auction_listing.id,)))
    

@login_required
def show_watchlist(request):
    auction_listings = WatchlistItem.return_auction_listings(request.user)
    return render(request, 'auctions/index.html', {
        'auction_listings': auction_listings
    })


def show_categories(request):
    categories = AuctionListingCategory.objects.all()
    return render(request, 'auctions/show_categories.html', {
        'categories': categories
    })

def show_category(request, category_id):
    category = AuctionListingCategory.objects.get(pk=category_id)
    auction_listings = AuctionListing.objects.filter(category=category)
    return render(request, 'auctions/index.html', {
        'auction_listings': auction_listings,
        'category': category
    })