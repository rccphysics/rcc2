from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("hello world")
    
def tasks(request):
    return HttpResponse("this is a list of qa tasks")
