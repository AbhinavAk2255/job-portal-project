from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.index),
    path('home/',views.home),
    path('about/',views.about),
    path('login/',views.login,name='login'),
    path('register/',views.register),
    path('forgote/',views.forgote,name='forgot_password'),
]