from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'Register.html')

def forgote(request):
    return render(request,'forgote.html')

def adminpanel(request):
    return render(request,'dashboard.html')

def employer(request):
    return render(request,'employee.html')

def user(request):
    return render(request,'user.html')