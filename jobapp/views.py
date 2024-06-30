from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'layout/base.html')

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

