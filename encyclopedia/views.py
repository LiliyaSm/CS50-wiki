from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.core.validators import RegexValidator
import markdown2
import re
import random

from . import util


class CreatePageForm(forms.Form):
    title = forms.CharField(label="Enter a title", max_length=30,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control mb-4'}),
                            validators=[RegexValidator('^[a-zA-Z0-9 -]{1,30}$', message="Title must be between 1 to 30 characters, contain only Latin letters, digits, dashes and spaces")])
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', "rows": "17"}), label="Enter a description", max_length=1000)


def index(request):
    """
    Renders list of all enries
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    """
    Renders HTML entry page 
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


def search_entry(request):
    """
    Search by title. Redirects to a search results page or, if a complete match, to 
    an entry page 
    """
    title = request.POST.get('q')
    entry = util.get_entry(title)
    list_titles = util.list_entries()

    if entry:
        # convert markdown into HTML
        entry = markdown2.markdown(entry)
        return redirect("entry", title)

    result = []
    for item in list_titles:
        if re.search(title, item, re.IGNORECASE):
            result.append(item)

    return render(request, "encyclopedia/search_results.html", {
        "name": title,
        "entries": result
    })


def new_page(request):
    """
    Renders page with form for creation new page
    """
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html", {
            "form": CreatePageForm()
        })
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if not form.is_valid():
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
        title = form.cleaned_data["title"]
        content = form.cleaned_data["description"]

        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            messages.add_message(request, messages.ERROR,
                                 'Entry already exists with the provided title!')
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
        else:
            util.save_entry(title, content)
            return redirect("entry", title)


def edit_page(request, title):
    """
    Renders page with forms for editing existing entries
    """
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "content": content})

    if request.method == "POST":
        content = request.POST.get("description")
        util.save_entry(title, content)
        return redirect("entry", title)


def random_page(request):
    """
    Redirects to a random page
    """
    list_entries = util.list_entries()
    title = random.choice(list_entries)
    return redirect("entry", title)
