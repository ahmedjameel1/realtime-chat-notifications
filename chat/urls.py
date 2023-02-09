from django.urls import path
from . import views

urlpatterns = [
    path('chat/<slug:room_slug>/', views.privateChat, name='private-chat'),
]
