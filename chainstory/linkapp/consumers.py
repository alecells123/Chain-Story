import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, User
from django.urls import reverse
from django.test import Client

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        if text_data_json.get('type') == 'reset':
            # Broadcast reset message to all clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': '',
                    'reset': True
                }
            )
            return
        
        # Handle different message types
        message_type = text_data_json.get('type')

        if message_type == 'request_history':
            # Send chat history
            messages = await self.get_chat_history()
            await self.send(text_data=json.dumps({
                'type': 'history',
                'messages': messages
            }))
            return

        # Handle regular chat messages
        message = text_data_json['message']
        name = text_data_json['name']
        color = text_data_json['color']

        # Save message to database
        await self.save_message(message, name, color)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "color": color
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        if event.get('reset'):
            await self.send(text_data=json.dumps({
                'type': 'reset'
            }))
            return
        
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_chat_history(self):
        messages = ChatMessage.objects.select_related('user').all().order_by('timestamp')
        return [{
            'content': msg.content,
            'color': msg.color,
            'username': msg.user.username
        } for msg in messages]

    @database_sync_to_async
    def save_message(self, message, name, color):
        user, _ = User.objects.get_or_create(
            username=name,
            defaults={'color': color}
        )
        # Update color if it changed
        if user.color != color:
            user.color = color
            user.save()
        
        return ChatMessage.objects.create(
            content=message,
            user=user,
            color=color  # Store current color with message
        )