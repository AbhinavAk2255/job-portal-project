from django.shortcuts import render

# Create your views here.

def adminpanel(request):
    return render(request,'dashboard.html')

def employer(request):
    return render(request,'employee.html')

def user(request):
    return render(request,'user.html')

def userDetails(request):
    return render(request,'user_details.html')

def employerDetails(request):
    return render(request,'employer_details.html')

def jobs(request):
    return render(request,'jobs.html')

def job_details(request):
    return render(request,'job_details.html')