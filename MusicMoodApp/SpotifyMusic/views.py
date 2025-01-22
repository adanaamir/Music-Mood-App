from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Helloooo")

def adan(request):
    return HttpResponse("its adan")

def greet(request, name):
    return HttpResponse(f"hey {name}!")
    