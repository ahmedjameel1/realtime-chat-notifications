from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Account
from chat.models import Room, Message
from channels.layers import get_channel_layer
import asyncio


@receiver(post_save, sender=Account)
def createRoom(sender, instance, created, **kwargs):
    if created:
        obj = instance
        chat_room = Room.objects.create(owner=obj)
        chat_room.slug = obj.username
        chat_room.save()


@receiver(post_save, sender=Message)
def messageSender(sender, instance, created, **kwargs):
    if created:
        obj = instance
        channel_layer = get_channel_layer()
        sender = obj.sender.username
        recipient = obj.recipient.username
        group_name = f"chat-{sender}-{recipient}"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(channel_layer.group_send(group_name, {
            'type': 'send_message',
            'message': obj.body,
            'sender': obj.sender.username,
            'recipient': obj.recipient.username
        }))
