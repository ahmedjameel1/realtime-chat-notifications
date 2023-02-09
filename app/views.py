from django.shortcuts import render
from .models import Notification

# Create your views here.


def index(request):
    try:
        notifications = Notification.objects.filter(
            user=request.user).order_by('-created_at')
    except:
        notifications = None
    username = request.user.username
    ctx = {
        'notifications': notifications, 'username': username
    }
    return render(request, 'app/index.html', ctx)
