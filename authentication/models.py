from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Hobbies(models.Model):
    Hobbie = models.CharField(max_length=255)

    def __str__(self):
        return self.Hobbie
    

class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class JobTitle(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    



class User(AbstractUser):
        

    GENDER_CHOICES = (
            ('M', 'Male'),
            ('F', 'Female'),
    )

    COUNTRY_CHOICES = (
            ('IN', 'india'),
    )

    QUALIFICATION_CHOICES = (

        ("High School", "High School"),
        ("Associate's Degree", "Associate's Degree"),
        ("Bachelor's Degree", "Bachelor's Degree"),
        ("Master's Degree", "Master's Degree"),
        ("Doctorate", "Doctorate"),
        ("Professional Degree", "Professional Degree"),
        ("Diploma", "Diploma"),
        ("Postdoctoral", "Postdoctoral"),
        ("Vocational", "Vocational"),
    )

    EXPERIANCE_LEVEL = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    )

    EMPLOYEE_TYPE = (
        ("job seeker", "JOB SEEKER"),
        ("employer", "EMPLOYER"),
    )

    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    Hobbies = models.ForeignKey(Hobbies, related_name='user_activities', on_delete=models.CASCADE, null=True, blank=True)
    Interest = models.ForeignKey(Interest, related_name='user_activities', on_delete=models.CASCADE, null=True, blank=True)
    short_bio = models.TextField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES)
    country = models.CharField(max_length=50, default='IN', choices=COUNTRY_CHOICES)
    open_to_hiring = models.BooleanField(default=False)
    smoking_habit = models.BooleanField(default=False)
    drinking_habit = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    images = models.ImageField('Image/', blank=True)
    short_reel = models.FileField(upload_to='short_reels/', blank=True)
    qualification = models.CharField(max_length=255, blank=True, null=True, choices=QUALIFICATION_CHOICES)

    employe = models.CharField(max_length=100, choices=EMPLOYEE_TYPE, null=True, blank=True)
    company_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE, null=True, blank=True)
    expertise_level = models.CharField(max_length=255, null=True, blank=True, choices=EXPERIANCE_LEVEL)

    # def __str__(self):
    #     return self username

    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return None
    


class Address(models.Model):

    COUNTRY_CHOICES = (
            ('IN', 'india'),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    address_line_1 = models.TextField(max_length=250)
    address_line_2 = models.TextField(max_length=250)
    address_line_3 = models.TextField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='IN', choices=COUNTRY_CHOICES)
    pincode = models.CharField(max_length=25)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_default = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'name']

    def __str__(self):
        return f'''{self.address_line_1}
        {self.address_line_2}
        {self.address_line_3}'''






class UserQualifications(models.Model):
    LEVEL_CHOICES = (
        ('high_school', 'High School'),
        ('diploma', 'Diploma'),
        ('ug', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('pg', 'Postgraduate'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, related_name='user_qualifications', on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    course = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.level} at {self.institution}"

    



class UserHobbie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobbie = models.ForeignKey(Hobbies, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hobbie')


class UserIntrests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'interest')






