from .models import NotificationList

def job_post(request):
    if request.user.is_authenticated:
        try:
            notifications = NotificationList.objects.filter(user=request.user,is_read = False).select_related('notification')
            count = notifications.count()
            return {'notifications': notifications,'count':count}
        except:
            return {'notifications': None}
    else:
        return {}
