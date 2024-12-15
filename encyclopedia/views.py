from django.shortcuts import render
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
