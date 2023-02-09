# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import Account


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        username = user.username
        self.group_name = f"notification-{username}"
        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification = text_data_json["notification"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name, {
                "type": "send_notification", "notification": notification}
        )

    # Receive message from room group
    async def send_notification(self, event):
        notification = event["notification"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"notification": notification}))
