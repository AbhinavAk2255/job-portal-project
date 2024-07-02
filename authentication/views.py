from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, View, FormView, UpdateView, TemplateView
from django.urls import reverse, reverse_lazy

# Create your views here.


class signout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse('accounts:login'))


class user_login(View):
    form_class = LoginForm
    template_name = 'user/login.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('Invalid username or password')
        return render(request, self.template_name, {'form': form})
    


class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'user/Register.html'
    success_url = reverse_lazy('accounts:user_activity')

    def get(self, request):
        
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()        
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        login(request, user)
        return redirect(reverse('accounts:user_activity'))
    
    

# class RegisterCompleteView(LoginRequiredMixin, View):
#     form_class = DetailRegistration
#     template_name = 'user/complete_register.html'
#     success_url = reverse_lazy('login')

#     def get(self, request):
#         return render(request, self.template_name, {'form': self.form_class()})
    
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if not form.is_valid():
#             return render(request, self.template_name, {'form': form})
        
#         user = self.request.user
        
#         user.phone = form.cleaned_data['phone']
#         user.dob = form.cleaned_data['dob']
#         user.short_bio = form.cleaned_data['short_bio']
#         user.job_title = form.cleaned_data['job_title']
#         user.gender = form.cleaned_data['gender']
#         user.country = form.cleaned_data['country']
#         user.open_to_hiring = form.cleaned_data['open_to_hiring']
#         if 'profile_photo' in form.cleaned_data:
#             user.profile_photo = form.cleaned_data['profile_photo']
#             user.save()

#         return redirect(reverse('home'))




class ActivitiesCreateView(LoginRequiredMixin, CreateView):
    model = UserActivity
    form_class = ActivitiesForm
    template_name = 'user/user_activities.html'
    success_url = reverse_lazy('accounts:user_seleciton')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class UserSelection(View):

    def get(self, request):
        return render(request, 'user/userSelection.html')



def CustomForgotPassword(request):
    
    context = {}

    if request.method == 'GET':
        context['form'] = ForgotePasswordForm()
        return render(request,'user/forgot_password.html',context)
    else:
        form = ForgotePasswordForm(data = request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if User is not None:
                current_site = get_current_site(request)
                mail_subject = 'Reset Your Password'
                message = render_to_string('user/reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.content_subtype = 'html'
                send_email.send()

                context = {
                    'email_sent': True,
                    'email': email,
                }
                messages.success(request, 'email send successsfuly')
                return redirect('password_reset_message')
            else:
                messages.error(request, 'Account does not exist.')
                return redirect('forgot_password')
        else:
            context['form'] = form
            return render(request,'user/forgot_password.html',context)
        

def emilamsg(request):
    return redirect(request, 'user/password_reset_sent.html')
        

def get_user(uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        return User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None
    
def reset_password(request, uidb64, token):
    user = get_user(uidb64)

    if request.method == 'GET':
        if user is not None and default_token_generator.check_token(user, token):
            form = ResetPassword()
            return render(request, 'user/reset_password.html', {'form': form})
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('login')

    elif request.method == 'POST':
        if user is not None and default_token_generator.check_token(user, token):
            form = ResetPassword(data = request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']

                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password reset successful. Please login with your new password.')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'user/reset_password.html', {'form': form})
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('login')



# Address creation view

class AddressListVew(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'accounts/address_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super(AddressListVew, self).get_queryset()
        return queryset.filter(user = self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    form_class = AddressCreationForm
    template_name = 'accounts/address_upsert.html'
    success_url = reverse_lazy('accounts:address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AddressCreationForm
    model = Address
    template_name = 'accounts/address_upsert.html'
    success_url = reverse_lazy('accounts:address_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user)



class AddressDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        address = get_object_or_404(Address, id=id, user = request.user)
        address.delete()
        return redirect('accounts:address_list')
    



# profile views

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_view.html'



class ProfileUpdateView(LoginRequiredMixin, FormView):
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile_view')

    def get_form_kwargs(self):
        form_args =  super().get_form_kwargs()
        form_args['instance'] = self.request.user
        return form_args
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

