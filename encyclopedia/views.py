from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.shortcuts import redirect
import markdown2
import re
import random
from django.core.files.storage import default_storage

from . import util


def index(request):
    """
    render list of all enries
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):    
    """
    render HTML entry page 
    """
    entry = util.get_entry(name)
    if not entry:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    # convert markdown into HTML
    entry = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry.html", {
    "name": name,
    "entry": entry
    })



def search_entry (request):
    title = request.POST.get('q')
    entry = util.get_entry(title)
    list_titles =  util.list_entries()

    if entry:
        entry = markdown2.markdown(entry)
        return  redirect("entry", title)
        
    result = []
    for item in list_titles:
        if re.search(title, item, re.IGNORECASE):
            result.append(item)

    return  render(request, "encyclopedia/search_results.html", {
        "name": title,
        "entries": result
        })



def new_page(request): 
    if request.method == "GET":   
        return render(request, "encyclopedia/new_page.html")
    if request.method == "POST":
        pattern = r'^[a-z0-9 -]{1,30}$'
        title = request.POST.get('title')
        content = request.POST.get("description")
        # check if form data is valid
        if not re.match(pattern, title, re.IGNORECASE):
            messages.add_message(request, messages.ERROR, 'Title must be between 1 to 30 characters, contain only Latin letters, digits, dashes and spaces')
            return render(request, "encyclopedia/new_page.html")
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            messages.add_message(request, messages.ERROR, 'Entry already exists with the provided title!')
            return render(request, "encyclopedia/new_page.html")
        else:
            util.save_entry(title, content)
            return redirect("entry", title)
        

def edit_page (request, title):
    if request.method == "GET":   
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title":title, "content" : content})

    if request.method == "POST":
        content = request.POST.get("description")
        util.save_entry(title, content)
        return redirect("entry", title)


def random_page(request):
    """
    redirect to a rendom page
    """
    list_entries = util.list_entries()
    title = random.choice(list_entries)
    return redirect("entry", title)
