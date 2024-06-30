from django.urls import path
from .views import *

urlpatterns = [
    path('login/',user_login.as_view(),name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register_profile/', RegisterCompleteView.as_view(), name='register_complete'),
    path('logout/',signout.as_view(),name='logout'),

    # default buid in reset_password urls

    # path('forgot_password/',views.CustomForgotPassword, name='forgot_password'),
    # path('reset-password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # custom forgot password urls

    path('forgot_password/', CustomForgotPassword, name='forgot_password'),
    path("reset-password/validate/<uidb64>/<token>/", reset_password, name='reset_password_validate'),
    path('reset-password_sent/', emilamsg, name='password_reset_message'),


    # address urls

    path('address/', AddressListVew.as_view(), name='address_list'),
    path('address/create/', AddressCreateView.as_view(), name='address_create'),
    path('address/update/<id>/', AddressUpdateView.as_view(), name='address_update'),
    path('address/delete/<id>/', AddressDeleteView.as_view(), name='address_delete'),

    # profile update url

    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update')

]

# template_name='user/password_reset.html'
# template_name='user/password_reset_sent.html'
# template_name='user/password_reset_form.html'
# template_name='user/password_reset_done.html'



