from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def signout(request):
    logout(request)
    return redirect('login')


def login(request):

    if request.POST:
        username = request.POST.get('Username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if(user):
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid User!")

    return render(request,'login.html')

def register(request):

    if request.POST:
        try:
            
            username = request.POST.get('Username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('repassword')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            success_message = 'successfuly registered....'
            messages.success(request,success_message)
            return redirect(login)

        except Exception as e:
            error_message = 'duplicate user or invalid credentials'
            messages.error(request,error_message) 

    return render(request,'Register.html')

def forgote(request):
    return render(request,'forgote.html')

