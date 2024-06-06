from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'base.html')

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'Register.html')

def forgote(request):
    return render(request,'forgote.html')