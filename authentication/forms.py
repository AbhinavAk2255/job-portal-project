from typing import Any
from django.forms import CharField, ModelForm, Form, EmailInput, PasswordInput, Select, RadioSelect, CheckboxInput, TextInput
from django.forms import  CharField, Textarea, FileInput, DateInput,NumberInput,IntegerField,ImageField,ClearableFileInput,ChoiceField,DateField,SelectMultiple
from .models import *
from django.core.validators import MinLengthValidator
from django import forms
from django.core.exceptions import ValidationError
from .validators import validate_video_file
from django.utils.translation import gettext_lazy as _


def validate_age(dob):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 18:
        raise ValidationError('You must be at least 18 years old.')


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

    def to_python(self, data):
        if data in self.empty_values:
            return None

        if isinstance(data, list):
            return [self.check_and_store_image(d) for d in data]
        else:
            return self.check_and_store_image(data)

    def check_and_store_image(self, data):
        file = super().to_python(data)
        if file is None:
            return None
        if not file.content_type.startswith('image'):
            raise ValidationError(_('File type is not supported.'), code='invalid')
        return file



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
        })
    )

    
    class Meta:
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
                
            }),

            'last_name': TextInput({
                'class':'form-control',
                
            }),

            'username': TextInput({
                'class':'form-control',
                
            }),

            'email': EmailInput({
                'class':'form-control',
                
            }),

            'password': PasswordInput({
                'class':'form-control',
                
            }),

        }

        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        print(password)
        print(confirm_password)

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
                

        return cleaned_data


#user activities form

class SecondRegistration(ModelForm):
    class Meta:
        model = User
        fields = ['date_of_birth', 'qualification', 'smoking_habit', 'drinking_habit', 'profile_picture', 'short_reel']

        
        widgets = {

            'date_of_birth' : DateInput({
                'class': 'form-control',
                'type' : 'date'
                
            }),
            'qualification' : Select({
                'class': 'form-control',
                'Placeholder' : 'Highest Qualification'
                
            }),

            'smoking_habit' : Select({
                
                
            }),
            'drinking_habit' : Select({
                
                
            }),
            'profile_picture' : FileInput({
                'class': 'form-control',
                
            }),

            'short_reel' : FileInput({
                'class': 'form-control',
                
            }),


        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.fields.items():
            field_instance.required = True
    
    def clean_dob(self):
        dob = self.cleaned_data.get('date_of_birth')
        validate_age(dob)
        return dob
    
    def clean_short_reel(self):
        short_reel = self.cleaned_data.get('short_reel', False)
        if not short_reel:
            raise forms.ValidationError("No file chosen!")

        validate_video_file(short_reel)
        return short_reel

class UserImageForm(ModelForm):
    image = MultipleImageField(label='Image Files')

    class Meta:
        model = UserImages
        fields = ['image']
        widgets = {
            'image': MultipleImageInput(attrs={'class': 'form-control', 'multiple': True,'accept': 'image/*'}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
    
class ImageForm(forms.ModelForm):
    
    class Meta:
        model = UserImages
        fields = ['image']
        
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'required':True}),
        }
        
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if not image:
            raise forms.ValidationError("File is required.")
        return image




class UserHobbyForm(ModelForm):
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobbies.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = UserHobbie
        fields = []


class UserInterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = UserIntrests
        fields = []





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
        fields = ['name','address_line_1','address_line_2','address_line_3','city','state','pincode','country','phone','is_default']
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
            'short_bio',
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
            'short_bio': Textarea({
                'class': 'form-control',
                'rows': '3'
            }),

            'gender': Select({
                'class': 'form-control'
            }),

            'country': Select({
                'class': 'form-control'
            }),

            'open_to_hiring': CheckboxInput(),
        }





# class QualificationsForm(ModelForm):
#     class Meta:
#         model = UserQualifications
#         exclude = ["user"]
        
#     def clean(self):
#         cleaned_data = super().clean()
#         start_date = cleaned_data.get('start_date')
#         end_date = cleaned_data.get('end_date')

#         if start_date and end_date:
#             if start_date >= end_date:
#                 raise forms.ValidationError("Start date must be earlier than end date.")

#         return cleaned_data


# empoloyer registration form

class EmployerRegisterForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['company_name', 'designation', 'location', 'employe']
        widgets = {
            'company_name' : TextInput({
                'class': 'form-control',
                
                
            }),
            'designation' : TextInput({
                'class': 'form-control',
                
                
            }),
            'location' : TextInput({
                'class': 'form-control',
                
                
            }),
            'employe' : Select({
                'class': 'form-control',
                
            }),

        }


class JobSeekerRegisterForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['job_title', 'expertise_level','employe']
        widgets = {
            'job_title' : Select({
                'class': 'form-control',
                'placeholder': 'Job Title'
                
            }),
            'expertise_level' : Select({
                'class': 'form-control',
                'placeholder': 'Expertise Level'
                
            }),
            'employe' : Select({
                'class': 'form-control',
                'placeholder': 'Who you Are'
                
            }),
        }


# job post form

