from pyexpat.errors import messages
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, View, FormView, UpdateView, TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import HttpResponse

# Create your views here.




class JobPost(LoginRequiredMixin, CreateView):
    model = Jobs
    form_class = JobPostingForm
    template_name = 'user/job_post.html'
    success_url = reverse_lazy('jobs:job_post')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company_name = self.request.user.company_name
        return super().form_valid(form)
    


# class JobListingView(LoginRequiredMixin, View):
#     template_name = 'home.html'


#     def get(self, request):
#         jobs = Jobs.objects.all().exclude(user= self.request.user).order_by('-id')[:4]
#         # jobs = Jobs.objects.order_by('-id').exclude(User=request.user)[:4]

#         job_id = request.GET.get('jobs','')
#         job_description = None
#         if job_id:
#             job_description = Jobs.objects.get(pk=job_id)
            

#         context = {
#             'jobs':jobs,
#             'job_description':job_description,
#         }

#         return render(request,self.template_name,context)
    

class JobsListingView(LoginRequiredMixin, View):
    template_name = 'home.html'
    paginate_by = 4
    

    def get(self, request):
        search_querry = request.GET.get('search', '')

        if search_querry:
            job_list = Jobs.objects.filter(
                job_title__title__icontains = search_querry
            ).exclude(
                user= self.request.user
            ).order_by('-id')
        else:
            job_list = Jobs.objects.all().exclude(user= self.request.user).order_by('-id')
            

        
        job_id = request.GET.get('jobs','')
        job_description = None
        if job_id:
            job_description = Jobs.objects.get(pk=job_id)

        elif job_list.exists():
            job_description = job_list.first()
            

        paginator = Paginator(job_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        print(page_obj)

        context = {
            'jobs':page_obj,
            'job_description':job_description,
        }

        return render(request,self.template_name,context)


class JobPostedLists(LoginRequiredMixin, View):
    template_name = 'employer/jobs_posted_list.html'
    paginate_by = 3


    def get(self, request):
        # loged_user = self.request.user

        job_post = Jobs.objects.filter(user=self.request.user)
        all_applications = []
        
        if job_post.exists():
            for job in job_post:
                applications = JobApplication.objects.filter(job=job)
                all_applications.extend(applications)

        count = len(all_applications)
        context = {
            'jobs': job_post,
            'count':count
        }
        return render(request, self.template_name,context)
    


class JobApplyingView(LoginRequiredMixin, View):
    form_class = ApplicationForm
    template_name = 'application_form.html'

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        job = get_object_or_404(Jobs, id=id)
        context = {
            'job' : job,
            'form': self.form_class()
        }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        job = get_object_or_404(Jobs, id=id)
        context = {
            'job' : job,
            'form': self.form_class()
        }
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(form.errors)
            return render(request, self.template_name, context)
        
        form.instance.user = self.request.user
        form.instance.job = job

        form.save()
        return redirect(reverse('jobs:success'))
    
    


class ApplicationListView(LoginRequiredMixin, View):
    template_name = 'employer/applications_list.html'
    paginate_by = 2

    def get(self, request,  *args, **kwargs):
        job_id = kwargs.get('id')
        job = get_object_or_404(Jobs, id=job_id)

        if job.user != self.request.user:
            messages.error(request, 'You Do not have the permission!')
            return redirect(reverse('jobs:posted_jobs'))
        
        status_filter = request.GET.get('status', '')
        print(status_filter)
        job_applications = JobApplication.objects.filter(job=job) 
        

        if status_filter:
            job_applications = JobApplication.objects.filter(status=status_filter)


        paginator = Paginator(job_applications, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context = {
            'applications': page_obj,
            'job': job,
            'selected_status': status_filter,
            'status_choices' : JobApplication.STATUS_TYPE
        }
        return render(request, self.template_name, context)
    
    def post(self, request,  *args, **kwargs):
        job_id = kwargs.get('id')
        job = get_object_or_404(Jobs, id=job_id)

        if job.user != self.request.user:
            messages.error(request, 'You Do not have the permission!')
            return redirect(reverse('jobs:posted_jobs'))
        
        action = request.POST.get('action')
        application_id = request.POST.get('application_id')
        application = get_object_or_404(JobApplication, id=application_id, job=job)

        if action == 'Select':
            application.status = 'Selected'
        elif action == 'Reject':
            application.status = 'Rejected'

        
        application.save()
        page_number = request.GET.get('page', 1)
        status_filter = request.GET.get('status', '')

        redirect_url = f"{request.path}?page={page_number}&status={status_filter}"
        return redirect(redirect_url)




# class JobApplyingFormView(LoginRequiredMixin, View):
#     form_class = ApplicationForm
#     template_name = 'application_form.html'

#     def get(self, request):
#         return render(request, self.template_name, {'form':self.form_class()})
    
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if not form.is_valid():
#             return render(request, self.template_name, {'form':self.form_class()})
        
#         form.instance.user = self.request.user

#         form.save()
#         return redirect(reverse('jobs:success'))
    


class SuccessPageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'application_success.html')

    

class ChangeUserTypeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangeUserTypeForm
    template_name = 'home.html'
    success_url = reverse_lazy('base:home')

    def form_valid(self, form):
        previous_employe = self.object.employe
        response = super().form_valid(form)
        if previous_employe == 'employer' and form.cleaned_data['employe'] == 'job seeker':
            # User is changing from employer to job seeker
            Jobs.objects.filter(employer=self.object).delete()
            messages.success(self.request, 'Your status has been changed to job seeker and your posted jobs have been deleted.')
        elif previous_employe == 'job seeker' and form.cleaned_data['employe'] == 'employer':
            # User is changing from job seeker to employer
            messages.success(self.request, 'Your status has been changed to employer.')
        return response

    def get_object(self, queryset=None):
        return self.request.user