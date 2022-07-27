from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def page1(request):
    return HttpResponse("page1")

def page2(request):
    return HttpResponse("page2")

def page3(request):
    return HttpResponse("page3")

def page4(request):
    return HttpResponse("page4")