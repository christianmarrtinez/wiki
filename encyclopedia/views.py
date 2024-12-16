from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    # Get the content of the requested entry
    content = util.get_entry(title)
    
    # If the entry exists, convert it to HTML
    if content:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    else:
        # If the entry does not exist, return a 404 error
        raise Http404("Page not found.")

def search(request):
    query = request.GET.get("q", "").lower()  # Retrieve the query from the GET request
    entries = util.list_entries()  # Get all encyclopedia entries
    matches = [entry for entry in entries if query in entry.lower()]  # Substring matching

    if query in [entry.lower() for entry in entries]:  # Exact match
        return redirect("entry_page", title=query.capitalize())  # Redirect to the entry page
    
    # Render search results template with matching entries
    return render(request, "encyclopedia/search.html", {
        "matches": matches,
        "query": query
    })

def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Check if the entry already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "error": "An entry with this title already exists.",
                "title": title,
                "content": content
            })
        
        content_with_title = f"# {title}\n\n{content}"

        # Save the new entry
        util.save_entry(title, content_with_title)
        return redirect("entry_page", title=title)

    return render(request, "encyclopedia/create.html")

def edit_page(request, title):
    # Get the current content of the entry
    content = util.get_entry(title)

    if request.method == "POST":
        # Get the updated content from the form
        new_content = request.POST["content"]

        # Save the updated content
        util.save_entry(title, new_content)

        # Redirect to the updated entry page
        return redirect(f"/wiki/{title}")

    else:
        # Render the edit page with the existing content pre-filled
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })