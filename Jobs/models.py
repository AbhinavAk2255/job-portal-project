from django.db import models
from authentication.models import User,JobTitle



# Create your models here.

class Jobs(models.Model):

    JOB_TYPES = (
        ('Full Time', 'Full-Time'),
        ('Part Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship')
    )
    SALARY_TYPE = (
        ('Month', 'Month'),
        ('Year', 'Year')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    Description = models.TextField()
    company_name = models.CharField(max_length=255, null=True, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    job_mode = models.CharField(max_length=100, choices=JOB_TYPES, default='FT')
    vacancies = models.PositiveIntegerField()
    salary_type = models.CharField(max_length=255, choices=SALARY_TYPE, default='mnt')
    location = models.CharField(max_length=255, null=True)



class JobApplication(models.Model):

    STATUS_TYPE = (
        ('select', 'Select'),
        ('reject', 'Reject'),
        ('pending', 'Pending'),
    )

    QUIT_REASONS = (
    ('career_advancement', 'Career Advancement Opportunities'),
    ('better_compensation', 'Better Compensation and Benefits'),
    ('work_life_balance', 'Work-Life Balance'),
    ('relocation', 'Relocation'),
    ('further_education', 'Pursuing Further Education'),
    ('new_challenges', 'Seeking New Challenges'),
    ('company_culture', 'Company Culture'),
    ('health_reasons', 'Health Reasons'),
    ('personal_reasons', 'Personal Reasons'),
    ('family_commitments', 'Family Commitments'),
    ('retirement', 'Retirement'),
    ('contract_ended', 'Contract Ended'),
    ('career_change', 'Change in Career Path'),
    ('lack_of_growth', 'Lack of Professional Growth'),
    ('work_environment', 'Unsatisfactory Work Environment'),

    )
    
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, unique=True)
    designation = models.CharField(max_length=255, null=True)
    salary = models.IntegerField()
    quit_reason = models.CharField(max_length=255, choices=QUIT_REASONS, default='career_advancement')
    status = models.CharField(max_length=20, choices=STATUS_TYPE, default='pending')