from django.shortcuts import render, redirect
# Para usar las built-in functions:
from . import util
# Para realizar la conversión a html de los archivos .md:
import markdown2
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
from random import randint

class SearchForm(forms.Form):
    search = forms.CharField(label="Search Encyclopedia")

class NewEntryForm(forms.Form):
    title =  forms.CharField(widget=forms.TextInput(attrs={'name':'title'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':5,'cols':5,'class': 'form-control'}))


def index(request):
    search_form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : search_form
    })

def entry(request,title):
        return render(request,"encyclopedia/entry.html",{
            "entry_name" : title,
            "entry_content" : markdown2.markdown(util.get_markdown_text(title))
        })

def search(request):
    # Implementado con una clase SearchForm
    if request.method == "POST":  # Si se postea
        query = SearchForm(request.POST) # Me guardo el query como un objeto SearchForm

        if query.is_valid(): # Si el posteo es valido (ejemplo, no está vacío)

            if util.get_entry(query.cleaned_data['search']) is not None: # Verifico si el posteo esta en la lista de entries
                return HttpResponseRedirect(f"wiki/{query.cleaned_data['search']}") # Redirijo
            
            found_entries = list() # Si no entre antes, entonces veo si algun substring corresponde a algun entry
            for entry in util.list_entries():
                if entry.lower().find(query.cleaned_data['search']) != -1: 
                    found_entries.append(entry)
            
            if found_entries: # Si encontre algo, muestro los resultados parecidos
                return render(request, "encyclopedia/search.html", {
                    "results": found_entries,
                })
            else: 
                return render(request, "encyclopedia/search.html", {
                    "results": '',
                    "no_result": "No similar results found"
                })


def new(request):
    # Implementado a partir de leer un POST request
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if title == "" or content == "":
            return render(request, "encyclopedia/new_entry.html", 
            {"message": "Can't save with empty field.",
            "title": title, "content": content})

        if title in util.list_entries():
            return render(request, "encyclopedia/new_entry.html", 
            {"message": "Title already exist. Try another.", 
            "title": title, "content": content})

        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/new_entry.html")


def edit(request,title): 

    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html",
            {"message": "Can't save with empty field.",
            "title": title, "content": content
            })

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/edit.html",
     {'content': content,
      'title': title
      })

def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=random_title)

