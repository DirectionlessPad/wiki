from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import markdown
from . import util

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "search"
            visible.field.widget.attrs['placeholder'] = "Search Encyclopedia"
    search = forms.CharField(label="")

class SaveEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

def edit_entry_form(md):
    class EditEntryForm(forms.Form):
        content = forms.CharField(widget=forms.Textarea(), initial=md)
    return EditEntryForm


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm,
    })

def entry(request, entry_name):
    md = util.get_entry(entry_name)
    print(entry_name)
    if md:
        html = markdown(md)
    else:
        html = None
    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(),
        "entry": entry_name,
        "html": html,
        "form": SearchForm,
    })

def searchresults(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            searchresult=form.cleaned_data["search"]
        else:
            searchresult=None

    encyclopedia_entries = util.list_entries()
    if searchresult.lower() in [x.lower() for x in encyclopedia_entries]:
        return HttpResponseRedirect(reverse("title", args=[searchresult]))
    else:
        results = []
        for entry in encyclopedia_entries:
            if searchresult.lower() in entry.lower():
                results.append(entry)
        if results:
            return render(request, "encyclopedia/index.html", {
                "entries": results,
                "form": SearchForm,
            })
        else:
            return HttpResponseRedirect(reverse("title", args=["entry_not_found"]))

def newpage(request):
    filename = None
    if request.POST:
        form = SaveEntryForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data["content"]
        filename = content.split('\n',1)[0]
        filename = ''.join(filter(str.isalnum, filename))
        if filename.lower() not in [x.lower() for x in util.list_entries()]:
            util.save_entry(filename, content)
            return HttpResponseRedirect(reverse("title", args=[filename]))
        
    return render(request, "encyclopedia/newpage.html", {
        "entries": util.list_entries(),
        "form": SearchForm,
        "content": SaveEntryForm,
        "filename": filename,
    })

def editpage(request, entry_name):
    if request.POST:
        form = SaveEntryForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data["content"]
        util.save_entry(entry_name, content)
        return HttpResponseRedirect(reverse("title", args=[entry_name]))
    entry = util.get_entry(entry_name)
    editform = edit_entry_form(entry)
    return render(request, "encyclopedia/editpage.html", {
        "entries": util.list_entries(),
        "entry": entry_name,
        "form": SearchForm,
        "editform": editform,
    })