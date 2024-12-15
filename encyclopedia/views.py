from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title) ## Retrieve Markdown content ##
    if content is None:
        # if the entry doesn't exist, render an error page
        return render(request, "encyclopedia.error.html", {
            "message": f"'{title}' entry not found."
        })
    else:
        # convert Markdown to HTML
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
