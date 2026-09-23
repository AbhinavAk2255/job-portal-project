from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Jobs,Notification,NotificationList
from authentication.models import User

@receiver(post_save, sender=Jobs)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            subject = f'New Job Posting:{instance.job_title.title}',
            content=f'A new job posting has been added: {instance.job_title.title}'
        )
        try:
            
            job_profiles = User.objects.filter(job_title = instance.job_title, employe='job seeker')

            for job_profile in job_profiles:

                NotificationList.objects.get_or_create(user=job_profile, notification=notification)

        except User.DoesNotExist:
            pass