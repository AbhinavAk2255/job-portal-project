from typing import Any
from django.forms import ModelForm, Form, EmailInput, Select, RadioSelect, CheckboxInput
from django.forms import TextInput, PasswordInput, CharField, Textarea, FileInput, DateInput
from .models import *
from django.core.validators import MinLengthValidator
from django import forms


class LoginForm(Form):
    username = CharField(
        max_length = 15,
        min_length = 4,
        required = True,
        widget = TextInput({
            'class': 'form-control',
            'placeholder':'Username'
        })
    )

    password = CharField(
        max_length = 15,
        min_length = 4,
        required = True,
        widget = PasswordInput({
            'class': 'form-control',
            'placeholder':'Password'
        })
    )


class UserRegisterForm(ModelForm):

    confirm_password = CharField(
        max_length=25,
        min_length=8,
        required=True,
        validators=[
            MinLengthValidator(8,'Password is too short!')
        ],
        widget= PasswordInput({
            'class':'form-control',
            'placeholder':'Confirm Password'
        })
    )

    
    class Meta():
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        ]
        
        widgets = {
            'first_name': TextInput({
                'class':'form-control',
                'placeholder':'Firstname'
            }),

            'last_name': TextInput({
                'class':'form-control',
                'placeholder':'Lastname'
            }),

            'username': TextInput({
                'class':'form-control',
                'placeholder':'Username'
            }),

            'email': EmailInput({
                'class':'form-control',
                'placeholder':'Email'
            }),

            'password': PasswordInput({
                'class':'form-control',
                'placeholder':'Password'
            })
        }


class UserRegistrationCompleteForm(ModelForm):
    class Meta():
        model = User
        fields = [
            'phone',
            'profile_photo',
            'dob',
            'short_bio',
            'job_title',
            'gender',
            'country',
            'open_to_hiring'
        ]
        
        widgets = {

            'phone': TextInput({
                'class':'form-control',
                'placeholder':'Phone'
            }),

            'dob': DateInput({
                'class': 'form-control'
            }),

            'short_bio': Textarea({
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Short Bio'
            }),

            'job_title': TextInput({
                'class': 'form-control',
                'placeholder': 'Job Title'
            }),

            'gender': Select({
                'class': 'form-control'
            }),

            'country': Select({
                'class': 'form-control'
            }),

            'open_to_hiring': CheckboxInput(),

            'profile_photo': FileInput({
                'class': 'form-control'
            })
        }
    



class ForgotePasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )

# reset password form
class ResetPassword(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        label='Confirm Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    

    # Address creation form

class AddressCreationForm(ModelForm):

    class Meta:
        model = Address
        fields = '__all__'
        exclud = ['user']
        widgets = {
            'name': TextInput({
                'class': 'form-control'
            }),

            'address_line_1': TextInput({
                'class': 'form-control'
            }),

            'address_line_2': TextInput({
                'class': 'form-control'
            }),

            'address_line_3': TextInput({
                'class': 'form-control'
            }),

            'city': TextInput({
                'class': 'form-control'
            }),

            'state': TextInput({
                'class': 'form-control'
            }),

            'pincode': TextInput({
                'class': 'form-control'
            }),

            'country': Select({
                'class': 'form-control'
            }),

            'phone': TextInput({
                'class': 'form-control'
            }),

            'is_default': CheckboxInput(),
        }


# profile creation form

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'profile_photo',
            'dob',
            'short_bio',
            'job_title',
            'gender',
            'country',
            'open_to_hiring'
        ]

        widgets = {
            'username': TextInput({
                'class': 'form-control'
            }),

            'email': EmailInput({
                'class': 'form-control'
            }),
            
            'first_name': TextInput({
                'class': 'form-control'
            }),

            'last_name': TextInput({
                'class': 'form-control'
            }),

            'phone': TextInput({
                'class': 'form-control'
            }),

            'dob': TextInput({
                'class': 'form-control'
            }),

            'short_bio': Textarea({
                'class': 'form-control',
                'rows': '3'
            }),

            'job_title': TextInput({
                'class': 'form-control',
            }),

            'gender': Select({
                'class': 'form-control'
            }),

            'country': Select({
                'class': 'form-control'
            }),

            'open_to_hiring': CheckboxInput(),

            'profile_photo': FileInput({
                'class': 'form-control'
            })
        }