from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin-panel/',views.adminpanel,name='adminpanel'),
    path('admin-panel/employer',views.employer,name='employer'),
    path('admin-panel/user',views.user,name='user'),
    path('admin-panel/userdetails',views.userDetails,name='user_details'),
    path('admin-panel/employerdetails',views.employerDetails,name='employer_details'),
    path('admin-panel/jobs',views.jobs,name='jobs_lists'),
    path('admin-panel/jobsDetails',views.job_details,name='job_details'),
]