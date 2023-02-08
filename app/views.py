from django.shortcuts import render
from .models import Notification

# Create your views here.


def index(request):
    notifications = Notification.objects.all()
    ctx = {
        'notifications': notifications,

    }
    return render(request, 'app/index.html', ctx)
