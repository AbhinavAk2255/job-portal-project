from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.index),
    path('home/',views.home),
    path('about/',views.about),
]