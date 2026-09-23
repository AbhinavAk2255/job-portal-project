from datetime import date
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save


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

    SMOKING_CHOICES = (
    ('Non-smoker', 'Non-smoker'),
    ('Occasional smoker', 'Occasional smoker'),
    ('Regular smoker', 'Regular smoker'),
    ('Heavy smoker', 'Heavy smoker'),
    ('Trying to quit', 'Trying to quit'),
    )

    DRINKING_CHOICES = (
    ('Non-drinker', 'Non-drinker'),
    ('Occasional drinker', 'Occasional drinker'),
    ('Social drinker', 'Social drinker'),
    ('Regular drinker', 'Regular drinker'),
    ('Heavy drinker', 'Heavy drinker'),
    ('Trying to quit', 'Trying to quit'),
    )

    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    short_bio = models.TextField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES)
    country = models.CharField(max_length=50, default='IN', choices=COUNTRY_CHOICES)
    open_to_hiring = models.BooleanField(default=False)
    smoking_habit = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='Non-smoker')
    drinking_habit = models.CharField(max_length=20, choices=DRINKING_CHOICES, default='Non-drinker')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    short_reel = models.FileField(upload_to='short_reels/', blank=True)
    qualification = models.CharField(max_length=255, blank=True, null=True, choices=QUALIFICATION_CHOICES)

    employe = models.CharField(max_length=100, choices=EMPLOYEE_TYPE, null=True, blank=True)
    company_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE, null=True, blank=True)
    expertise_level = models.CharField(max_length=255, null=True, blank=True, choices=EXPERIANCE_LEVEL)


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






class Education(models.Model):

    QUALIFICATION_CHOICES = (
    ("High School", "High School"),
    ("Associate's Degree", "Associate's Degree"),
    ("Bachelor's Degree", "Bachelor's Degree"),
    ("Master's Degree", "Master's Degree"),
    ("Doctorate", "Doctorate"),
    ("Professional Degree", "Professional Degree"),
    ("Certificate", "Certificate"),
    ("Diploma", "Diploma"),
    ("Postdoctoral", "Postdoctoral"),
    ("Vocational", "Vocational"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=25, choices=QUALIFICATION_CHOICES)
    field_of_study = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.degree} from {self.institution}"

    



class UserHobbie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobbie = models.ForeignKey(Hobbies, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hobbie')

    def __str__(self):
        return f"{self.user.username} - {self.hobbie.Hobbie}"


class UserIntrests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'interest')

    def __str__(self):
        return f"{self.user.username} - {self.interest.name}"



class UserImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
    
@receiver(pre_delete, sender=UserImages)
def user_images_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=UserImages)
def user_images_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = UserImages.objects.get(pk=instance.pk)
            if old_instance.image:
                if old_instance.image != instance.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
        except UserImages.DoesNotExist:
            pass
    





class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
    

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class UserSkill(models.Model):

    LEVEL_CHOICES = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=12, choices=LEVEL_CHOICES)
    
    class Meta:
        unique_together = ['user', 'skill']
    
    def __str__(self):
        return f"{self.skill}"