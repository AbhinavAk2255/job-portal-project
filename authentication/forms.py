from django.forms import ModelForm, Form
from django.forms import TextInput, PasswordInput, CharField,EmailInput
from .models import *
from django.core.validators import MinLengthValidator



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
        model = user
        fields = ['email','username','password']
        widgets = {
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
