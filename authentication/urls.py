from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('forgote/',views.forgote,name='forgot_password'),
    path('logout/',views.signout,name='logout')
]