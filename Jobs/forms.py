from django.forms import DateInput, ModelForm, NumberInput, Select, TextInput, Textarea, SelectMultiple, FileInput
from Jobs.models import Jobs,  JobApplication
from tinymce.widgets import TinyMCE


class JobPostingForm(ModelForm):

    class Meta:
        model = Jobs
        fields = '__all__'
        exclude = ['user']
        widgets = {

            'job_title' : Select({
                'class': 'form-control',
                
            }),
            'Description' : TinyMCE(attrs={'cols': 80, 'rows': 10}),
            
            'company_name' : TextInput({
                'class': 'form-control',
                'placeholder': 'Company Name',
                'disabled': 'disabled'
                
            }),
            'salary_min' : NumberInput({
                'class': 'form-control',
                'placeholder': 'Salary Minimum',                
            }),
            'salary_max' : NumberInput({
                'class': 'form-control',
                'placeholder': 'Salary Maximum',                
            }),
            'application_deadline' : DateInput({
                'class': 'form-control',
                'placeholder': 'Application End date',   
                'type' : 'date'             
            }),
            'job_mode' : Select({
                'class': 'form-control',
                'placeholder': 'Job Mode',                
            }),
            'vacancies' : NumberInput({
                'class': 'form-control',
                'placeholder': 'Vacancies',                
            }),
            'salary_type' : Select({
                'class': 'form-control',  
                'placeholder': 'Salary Type', 
                            
            }),
            'location' : TextInput({
                'class': 'form-control',  
                'placeholder': 'Location', 
                            
            }),
        }


class ApplicationForm(ModelForm):

    class Meta:
        model = JobApplication
        fields = ['name', 'company', 'designation', 'salary', 'quit_reason', 'resume']
        widgets = {
            'name' : TextInput({
                'class': 'form-control',
                
            }),
            'company' : TextInput({
                'class': 'form-control',
                
            }),
            'designation' : TextInput({
                'class': 'form-control',
            }),
            'salary' : NumberInput({
                'class': 'form-control',
                
            }),
            'quit_reason' : Select({
                'class': 'form-control',
                
            }),
            'resume' : FileInput({
                'class': 'form-control',
                
            }),
            
            
        }