from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req,"index.html")

def bookshelf(req):
    return render(req,"bookshelf.html")