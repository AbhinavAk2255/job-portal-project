from urllib import request
from django.db import IntegrityError
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
                return redirect('base:home')
            else:
                return HttpResponse('Invalid username or password')
        return render(request, self.template_name, {'form': form})
    


# Register page 1

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

        if user is not None:
            login(request, user)
            messages.success(request, "Registration Step-1 Completed")
            return redirect(self.success_url)
        else:
            messages.error(request, "Authentication failed.")
            return render(request, self.template_name, {'form': form})
        

    
# Register page 2

class RegisterCompleteView(LoginRequiredMixin, FormView):
    form_class = SecondRegistration
    template_name = 'user/user_activities.html'
    success_url = reverse_lazy('accounts:user_seleciton')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hobby_form'] = UserHobbyForm()
        context['interest_form'] = UserInterestForm()
        context['image_form'] = UserImageForm()
        return context

    

    def form_valid(self, form):
        # Initialize forms with POST data
        hobby_form = UserHobbyForm(self.request.POST)
        interest_form = UserInterestForm(self.request.POST)
        image_form = UserImageForm(self.request.POST, self.request.FILES)

        if hobby_form.is_valid() and interest_form.is_valid() and image_form.is_valid() and form.is_valid():

            hobbies = hobby_form.cleaned_data['hobbies']
            for hobby in hobbies:
                UserHobbie.objects.get_or_create(user=self.request.user, hobbie=hobby)

            interests = interest_form.cleaned_data['interests']
            for interest in interests:
                UserIntrests.objects.get_or_create(user=self.request.user, interest=interest)

            images = self.request.FILES.getlist('image')
            for image in images:
                UserImages.objects.create(user=self.request.user, image=image)
            
            user = self.request.user
            user.profile_picture = form.cleaned_data['profile_picture']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.qualification = form.cleaned_data['qualification']
            user.smoking_habit = form.cleaned_data['smoking_habit']
            user.drinking_habit = form.cleaned_data['drinking_habit']
            user.short_reel = form.cleaned_data['short_reel']

            user.save()
            
            messages.success(self.request, "Registration Successfull")
            return super().form_valid(form)
        
        return self.form_invalid(form, hobby_form=hobby_form, interest_form=interest_form, image_form=image_form)
    
    def form_invalid(self, form, hobby_form=None, interest_form=None, image_form=None):
        context = self.get_context_data(
            form=form,
            hobby_form=hobby_form or UserHobbyForm(),
            interest_form=interest_form or UserInterestForm(),
            image_form=image_form or UserImageForm(),
        )
        messages.error(self.request, "Registration Unsuccessfull")
        return self.render_to_response(context)

    
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if not form.is_valid():
    #         return render(request, self.template_name, {'form': form})
        
    #     user = self.request.user
        
    #     user.date_of_birth = form.cleaned_data['date_of_birth']
    #     user.qualification = form.cleaned_data['qualification']
    #     user.smoking_habit = form.cleaned_data['smoking_habit']
    #     user.drinking_habit = form.cleaned_data['drinking_habit']
    #     if 'profile_picture' in form.cleaned_data:
    #         user.profile_picture = form.cleaned_data['profile_picture']
    #         user.save()

    #     return redirect(reverse('accounts:user_seleciton'))




# class ActivitiesCreateView(LoginRequiredMixin, CreateView):
#     model = UserActivity
#     form_class = ActivitiesForm
#     template_name = 'user/user_activities.html'
#     success_url = reverse_lazy('accounts:user_seleciton')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)



class UserSelection(View):

    def get(self, request):
        return render(request, 'user/userSelection.html')






# Employer Register page

class EmployerRegisterView(LoginRequiredMixin, CreateView):

    form_class = EmployerRegisterForm
    template_name = 'user/employer_registration.html'
    # success_url = reverse_lazy('accounts:user_seleciton)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        
        user = self.request.user
        
        user.company_name = form.cleaned_data['company_name']
        user.designation = form.cleaned_data['designation']
        user.location = form.cleaned_data['location']
        user.employe = form.cleaned_data['employe']
        user.save()

        return redirect(reverse('jobs:job_post'))
    



# job seeker Register page

class JobSeekerRegisterView(LoginRequiredMixin, View):
    form_class = JobSeekerRegisterForm
    template_name = 'user/job_seeker_register.html'


    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        
        user = self.request.user
          
        user.job_title = form.cleaned_data['job_title']
        user.expertise_level = form.cleaned_data['expertise_level']
        user.employe = form.cleaned_data['employe']
        user.save()

        return redirect(reverse('base:home'))
    



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            user_image.user = request.user
            user_image.save()
            messages.success(request, 'Image updated successfully.')
            return redirect(reverse_lazy('accounts:profile_view'))
        else:
            context = self.get_context_data()
            context['image_form'] = form
            context['form_errors'] = True
            return self.render_to_response(context)


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
    


class DeleteImageView(LoginRequiredMixin, View):
    def get(self, request, pk):
        image = get_object_or_404(UserImages, pk=pk)
        
        if image.user == request.user:
            image.delete()
            messages.success(request, 'Image deleted successfully.')
        else:
            messages.error(request, 'You are not authorized to delete this image.')
        
        return redirect(reverse_lazy('accounts:profile_view'))




class AddHobbyView(LoginRequiredMixin, CreateView):
    model = UserHobbie
    form_class = UserHobbyAddForm
    template_name = 'accounts/hobbies-add.html'
    success_url = reverse_lazy('accounts:profile_view')
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'Hobby already exists in your profile.')
            return self.form_invalid(form)
        

class AddInterestView(LoginRequiredMixin, CreateView):
    model = UserIntrests
    form_class = UserInterestAddForm
    template_name = 'accounts/interest-add.html'
    success_url = reverse_lazy('accounts:profile_view')
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'Interest already exists in your profile.')
            return self.form_invalid(form)
        


class DeleteHobbyView(LoginRequiredMixin, View):
    model = UserHobbie
    success_url = reverse_lazy('accounts:profile_view')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        hobby_id = kwargs.get('id')
        hobby = get_object_or_404(UserHobbie, id=hobby_id, user=self.request.user)
        hobby.delete()
        messages.success(request, 'Hobby deleted successfully.')
        return redirect('accounts:profile_view')
    

class DeleteInterestView(LoginRequiredMixin, View):
    model = UserIntrests
    success_url = reverse_lazy('accounts:profile_view')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        interest_id = kwargs.get('id')
        interest = get_object_or_404(UserIntrests, id=interest_id, user=self.request.user)
        interest.delete()
        messages.success(request, 'Interest deleted successfully.')
        return redirect('accounts:profile_view')
    


class UserSkillCreateView(LoginRequiredMixin, CreateView):
    form_class = UserSkillUpsertForm
    template_name = 'accounts/skill_upsert.html'
    success_url = reverse_lazy('accounts:skill_list')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'"{form.instance.skill}" created successfully.')
            return response
        except IntegrityError:
            messages.error(self.request, f'"{form.instance.skill}" already exists.')
            return self.form_invalid(form)
        


class UserSkillListVew(LoginRequiredMixin, ListView):
    model = UserSkill
    template_name = 'accounts/skills_lists.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
    

class UserSkillDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        education = get_object_or_404(UserSkill, id=id, user=request.user)
        education.delete()
        messages.success(self.request, f'{education.skill} deleted successfully.')
        return redirect('accounts:skill_list')
    


class ExperienceCreateView(LoginRequiredMixin, CreateView):
    form_class = ExperienceUpsertForm
    template_name = 'accounts/experience_upsert.html'
    success_url = reverse_lazy('accounts:experience_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'"{form.instance.title}" Added successfully.')
        return response
    

class ExperienceListVew(LoginRequiredMixin, ListView):
    model = Experience
    template_name = 'accounts/experience_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        queryset = sorted(queryset, key=lambda experience: experience.start_date, reverse=True)
        return queryset
    

class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ExperienceUpsertForm
    model = Experience
    template_name = 'accounts/experience_upsert.html'
    success_url = reverse_lazy('accounts:experience_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'"{form.instance.title}" Added successfully.')
        return response
    

class ExperienceDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        experience = get_object_or_404(Experience, id=id, user=request.user)
        experience.delete()
        messages.success(self.request, f'"{experience.title}" deleted successfully.')
        return redirect('accounts:experience_list')



class EducationCreateView(LoginRequiredMixin, CreateView):
    form_class = EducationUpsertForm
    template_name = 'accounts/education_upsert.html'
    success_url = reverse_lazy('accounts:education_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Education Added successfully.')
        return response
    


class EducationListVew(LoginRequiredMixin, ListView):
    model = Education
    template_name = 'accounts/education_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        queryset = sorted(queryset, key=lambda education: education.start_date, reverse=True)
        return queryset
    

class EducationUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EducationUpsertForm
    model = Education
    template_name = 'accounts/education_upsert.html'
    success_url = reverse_lazy('accounts:education_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Education Added successfully.')
        return response
    

class EducationDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        education = get_object_or_404(Education, id=id, user=request.user)
        education.delete()
        messages.success(self.request, f'Education deleted successfully.')
        return redirect('accounts:education_list')
