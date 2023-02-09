# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import Account


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        user = self.scope['user']
        username = user.username
        roomname = self.scope["url_route"]["kwargs"]['roomname']
        self.group_name = f"chat-{username}-{roomname}"
        self.opposite = f"chat-{roomname}-{username}"
        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add(self.opposite, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_discard(self.opposite, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,  {
                "type": "send_message", "message": message}
        )
        await self.channel_layer.group_send(
            self.opposite,  {
                "type": "send_message", "message": message}
        )

    # Receive message from room group
    async def send_message(self, event):
        message = event["message"]
        sender = event['sender']
        recipient = event['recipient']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, 'sender': sender,
                                              'recipient': recipient}))
