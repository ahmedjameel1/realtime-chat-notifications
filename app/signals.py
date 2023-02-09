from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from channels.layers import get_channel_layer
import asyncio
from accounts.models import Account


@receiver(post_save, sender=Notification)
def notificationSend(sender, instance, created, **kwargs):
    if created:
        obj = instance
        channel_layer = get_channel_layer()
        username = obj.user.username
        group_name = f"notification-{username}"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(channel_layer.group_send(group_name, {
            'type': 'send_notification',
            'notification': obj.text,
        }))
        print(group_name, obj.user)
