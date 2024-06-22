from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.

@login_required
def signout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request,'login.html',context)
    elif request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user,)
                return HttpResponseRedirect('home')
            else:
                return HttpResponse('invalid user')
            
        context['form'] = form
        return render(request,'login.html',context)
    



def register(request):
    context = {
        'form':UserRegisterForm(),
    }

    

    # if request.POST:
    #     try:
            
    #         username = request.POST.get('Username')
    #         email = request.POST.get('email')
    #         password = request.POST.get('password')
    #         confirm_password = request.POST.get('repassword')

    #         user = User.objects.create_user(
    #             username=username,
    #             email=email,
    #             password=password
    #         )

    #         success_message = 'successfuly registered....'
    #         messages.success(request,success_message)
    #         return redirect(login)

    #     except Exception as e:
    #         error_message = 'duplicate user or invalid credentials'
    #         messages.error(request,error_message) 

    return render(request,'Register.html',context)

def forgote(request):
    return render(request,'forgote.html')

