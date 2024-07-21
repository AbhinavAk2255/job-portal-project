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
    paginate_by = 3
    

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
    def get(self, request):
        return render(request, 'employer/jobs_posted_list.html')
    

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
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, context)
        
        form.instance.user = self.request.user
        form.instance.job = job

        form.save()
        return redirect(reverse('jobs:success'))
    
    

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

    

