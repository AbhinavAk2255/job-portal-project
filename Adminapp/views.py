from django.shortcuts import render

# Create your views here.

def adminpanel(request):
    return render(request,'admin_panel/dashboard.html')

def employer(request):
    return render(request,'admin_panel/employee.html')

def user(request):
    return render(request,'admin_panel/user.html')

def userDetails(request):
    return render(request,'admin_panel/user_details.html')

def employerDetails(request):
    return render(request,'admin_panel/employer_details.html')

def jobs(request):
    return render(request,'admin_panel/jobs.html')

def job_details(request):
    return render(request,'admin_panel/job_details.html')