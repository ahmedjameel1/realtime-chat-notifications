from django.urls import re_path
from app.consumers import NotificationConsumer
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/notification/(?P<username>[^/]+)/', NotificationConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<roomname>[^/]+)/', ChatConsumer.as_asgi())
]
