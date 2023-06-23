import sys
import random
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create_entry(request):
    """
    View logic to handle displaying a form to create a new 
    entry (GET) or to save and redirect (POST)
    """
    if request.method == "GET":
        return render(request, "encyclopedia/create_entry.html")
    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['markdown_content']
        if util.get_entry(title):
            # Lookup suggested that 400 would be the appropriate HTTP response code.
            response = HttpResponse('Bad Request: Title already present.')
            response.status_code = 400
            return response

        result = util.save_entry(title, content)
        return HttpResponseRedirect(reverse("show_entry", args=(title,)))


def edit_entry(request, title):
    """
    View logic to handle displaying a form to edit an 
    entry (GET) or to save the update and redirect (POST)
    """
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "content": content
        })
    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['markdown_content']
        if util.get_entry(title):
            result = util.save_entry(title, content)
            return HttpResponseRedirect(reverse("show_entry", args=(title,)))
        else:
            response = HttpResponse('Bad Request: Title does not exist.')
            response.status_code = 400
            return response


def random_entry(request):
    """
    Retrieving a random entry from the available entries list using 
    a random integer
    """
    entries = util.list_entries()
    entry = entries[random.randint(0, len(entries)-1)]
    return HttpResponseRedirect(reverse("show_entry", args=(entry,)))



def show_entry(request, search_string):
    """
    """
    entry = util.get_entry(search_string)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "search_string": search_string,
            "entry": util.convert_md_to_html(entry)
        })
    else:
        return HttpResponseNotFound() 

    
def search_entries(request):
    if request.method == "GET":
        search_string = request.GET['q']
        if search_string:
            entry = util.get_entry(search_string)
            if entry:
                return render(request, "encyclopedia/entry.html", {
                    "search_string": search_string,
                    "entry": util.convert_md_to_html(entry)
                })
            else:
                results_list = util.search_entries(search_string)
                return render(request, "encyclopedia/search_results.html", {
                    "search_string": search_string,
                    "entries": results_list
                })

        else:
            response = HttpResponse('No search string supplied.')
            response.status_code = 204
            return response

    else:
        response = HttpResponse('Method not allowed.')
        response.status_code = 405
        return response