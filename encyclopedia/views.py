import random
import markdown

from django.urls import reverse
from django.shortcuts import redirect, render
from . import util
from django import forms

""" Form Class for Search Bar """

class SearchForm(forms.Form):
    search_form = forms.CharField(label='',widget=forms.TextInput(attrs={
        'placeholder':'Search Encyclopedia'})
        )

""" Form Class for New Entry """

class CreateForm(forms.Form):
    title = forms.CharField(label= "Title", widget=forms.TextInput(attrs={
        'class' : ' form-control col-md-10',
        'placeholder':'Enter Title',
        })
        )
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={
        'class' : 'form-control col-md-10',
        'placeholder':'Enter Markdown content',
        })
        )

""" Form class edit page"""

class EditForm(forms.Form):
    content = forms.CharField(label='',widget=forms.Textarea(attrs={ 
        'class' : 'form-control col-md-10',
        'placeholder':'Enter Markdown content'
        })
        )


""" INDEX PAGE """

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


""" SEARCH  """

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)

        # If form is valid get de data ready to logic
        if form.is_valid():      
            search_item = form.cleaned_data["search_form"]
            entry_list = util.list_entries()
            lower_list = [x.lower() for x in entry_list]
            substring = list()

            # If entry exists, redirect to entry view
            if search_item.lower() in lower_list:
                return redirect(reverse('entry', args=[search_item]))

            # otherwise return the substring               
            else:
                for item in lower_list:
                    if search_item.lower() in item.lower():
                        substring.append(item)
                if substring:
                    return render(request, "encyclopedia/search.html", {
                        "form": SearchForm(),
                        "item": search_item,
                        "list": substring,
                    })
                # else the entry is not found  
                else:
                    return render(request, "encyclopedia/error.html", {
                        "result": "doens't",
                        "form": SearchForm()
        }) 


""" NEW PAGE """

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)

        # If form is valid get de data ready to logic
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entry_list = util.list_entries()
            lower_list = [x.lower() for x in entry_list]

            # if title exist send the exist page
            if title.lower() in lower_list:
                return render(request, "encyclopedia/error.html", {
                    "result": "already",
                    "form": SearchForm()
                        })
            # else safe de entry and go to the new page
            else:
                util.save_entry(title, content)
                return redirect(reverse('entry', args=[title]))
                

    return render(request, "encyclopedia/create.html", {
        "form": SearchForm(),
        "createform": CreateForm()
        })



""" EDIT ENTRY """

def edit(request,title):
    # show the existing entry conten
    entry = util.get_entry(title)
    
    if request.method == "POST":
            form = EditForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data["content"]
                # save de modification return to edited page
                util.save_entry(title, content)
                return redirect(reverse('entry', args=[title]))

    return render(request, "encyclopedia/edit.html", {
                        "content" : EditForm(initial={'content': entry}),
                        "form": SearchForm()
        })






""" MARKDOWN ENTRIES """

def entry(request, title):
    # extraigo el archivo md como string de title  
    entry_md = util.get_entry(title)

    # if the entry not exist 
    if entry_md == None:
        return render(request, "encyclopedia/error.html", {
                        "result": "doens't",
                        "form": SearchForm()
        }) 
    #otherwise show the existing entry page
    else:
        entry_html = markdown.markdown(entry_md)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry_html,
            "form": SearchForm()
            })


""" RANDOM PAGE """

def random_page(request):

    titles = util.list_entries()
    random_choice = random.choice(titles)

    return redirect(reverse('entry', args=[random_choice]))

