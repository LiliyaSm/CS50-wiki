from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import markdown2
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
        entry = util.get_entry(name)
        if not entry:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
        "name": name,
        "entry": entry
    })



def search_entry (request):
    title = request.POST.get('q')
    entry = util.get_entry(title)
    list_titles =  util.list_entries()

    print(request.POST.get('q'))
    if entry:
        entry = markdown2.markdown(entry)
        return  render(request, "encyclopedia/entry.html", {
        "name": title,
        "entry": entry
        })
    result = []
    for item in list_titles:
        if re.search(title, item, re.IGNORECASE):
            result.append(item)

    return  render(request, "encyclopedia/search_results.html", {
        "name": title,
        "entries": result
        })



def new_page(request):    
        return render(request, "encyclopedia/new_page.html", {
        # "entries": util.list_entries()
    })

def random(request):
    return render(request, "encyclopedia/random.html", {
    # "entries": util.list_entries()
})