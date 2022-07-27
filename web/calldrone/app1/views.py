from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def page1(request):
    return render(request, 'app1/page1.html')

def page2(request):
    return render(request, 'app1/page2.html')

def page3(request):
    return render(request, 'app1/page3.html')

def page4(request):
    return render(request, 'app1/page4.html')