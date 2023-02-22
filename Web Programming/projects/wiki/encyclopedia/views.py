from django.shortcuts import render

import markdown

from . import util

import random

# define function for markdown2 via trentm
def convert_markdown(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
# define index function for homepage
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
# define entry function for entry route
def entry(request,title):
    htmlcontent = convert_markdown(title)
    if htmlcontent == None:
        # define and implement error route
        return render(request, "encyclopedia/error.html", {
            "errormessage": "Invalid entry. Entry does not exist."
        })
        # define entry route in entry function
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlcontent,
        })
# define search function
def search(request):
    # ensure POST method is used
    if request.method == "POST":
        # implement search query
        entry_search = request.POST['q']
        # convert to md
        entry_content = convert_markdown(entry_search)
        if entry_content != None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": entry_content
            })
        else:
            # implement substring for search recommendation
            all_entries = util.list_entries()
            recommended_search = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommended_search.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommended_search
            })

# define new page function
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        # implement post method
        title = request.POST['title']
        content = request.POST['content']
        # confirm it is not already an existing entry
        existing_entry = util.get_entry(title)
        if existing_entry != None:
            # print error if duplicate
                return render(request, "encyclopedia/error.html", {
                    "errormessage": "Invalid/Duplicate entry. Entry already exists."
            })
        else:
            # implement save route if not error
            util.save_entry(title, content)
            # convert to md
            entry_content = convert_markdown(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": entry_content
            })

# define random page function
def random_page(request):
    # call all entries
    all_entries = util.list_entries()
    # call random function from import random
    random_entry = random.choice(all_entries)
    # convert to md
    entry_content = convert_markdown(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": entry_content
     })

# define edit page function
def edit_page(request):
    # implement post method
    if request.method == "POST":
        title = request.POST['title']
        # get content from get_entry
        content = util.get_entry(title)
    return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": content
    })

# define save edit page function
def save(request):
    # implement post method
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        # call save_entry function
        util.save_entry(request, content)
        # convert to md
        entry_content = convert_markdown(title)
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": entry_content
        })