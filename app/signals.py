from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from channels.layers import get_channel_layer
import asyncio


@receiver(post_save, sender=Notification)
def notificationSend(sender, instance, created, **kwargs):
    if created:
        obj = Notification.objects.filter(text__iexact=instance.text)[0].text
        channel_layer = get_channel_layer()
        group_name = 'notification'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(channel_layer.group_send(group_name, {
            'type': 'send_notification',
            'notification': obj
        }))
