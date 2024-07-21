from django.urls import path
from .views import *


app_name = 'jobs'

urlpatterns = [

    path('jobpost/', JobPost.as_view(), name='job_post'),
    path('posted_jobs/', JobPostedLists.as_view(), name='posted_jobs'),
    path('job_applying/<id>/', JobApplyingView.as_view(), name='job_applying'),
    path('success_page/', SuccessPageView.as_view(), name='success'),

]