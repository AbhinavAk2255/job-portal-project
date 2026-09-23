from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/',user_login.as_view(),name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user_activities/',RegisterCompleteView.as_view(), name='user_activity'),
    path('userselection/', UserSelection.as_view(), name='user_seleciton'),
    path('employer/register/', EmployerRegisterView.as_view(), name='employer_register'),
    path('jobseeker/register/', JobSeekerRegisterView.as_view(), name='jobseeker_register'),
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
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    


    path('adding_hobbies/', AddHobbyView.as_view(), name='adding_hobbies'),
    path('adding_interest/', AddInterestView.as_view(), name='adding_interest'),
    path('delete_hobbie/<id>', DeleteHobbyView.as_view(), name='delete_hobbie'),
    path('delete_interest/<id>', DeleteInterestView.as_view(), name='delete_interest'),
    path('delete_image/<int:pk>/', DeleteImageView.as_view(), name='delete_image'),


    path('skill/', UserSkillListVew.as_view(), name='skill_list'),
    path('skill/create/', UserSkillCreateView.as_view(), name='skill_create'),
    path('skill/delete/<id>/', UserSkillDeleteView.as_view(), name='skill_delete'),


    path('experience/', ExperienceListVew.as_view(), name='experience_list'),
    path('experience/create/', ExperienceCreateView.as_view(), name='experience_create'),
    path('experience/update/<id>/', ExperienceUpdateView.as_view(), name='experience_edit'),
    path('experience/delete/<id>/', ExperienceDeleteView.as_view(), name='experience_delete'),


    path('education/', EducationListVew.as_view(), name='education_list'),
    path('education/create/', EducationCreateView.as_view(), name='education_create'),
    path('education/update/<id>/', EducationUpdateView.as_view(), name='education_edit'),
    path('education/delete/<id>/', EducationDeleteView.as_view(), name='education_delete'),

]





