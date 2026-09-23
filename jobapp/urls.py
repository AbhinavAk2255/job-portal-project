from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from Jobs.views import *

app_name = 'base'

urlpatterns = [
    path('',views.index, name='index'),
    path('home/',JobsListingView.as_view(),name='home'),
    path('about/',views.about,name='about'),
]