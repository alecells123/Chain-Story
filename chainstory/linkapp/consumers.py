from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the chat group
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()
        
        # Get messages using sync_to_async
        from .models import ChatMessage  # Import here to avoid circular import
        get_messages = sync_to_async(lambda: list(ChatMessage.objects.all()))
        messages = await get_messages()
        
        # Send existing messages
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.content
            }))

    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        from .models import ChatMessage
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message using sync_to_async
        save_message = sync_to_async(ChatMessage.objects.create)
        await save_message(content=message)

        # Send message to chat group
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat_message",
                "message": message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def get_chat_messages(self):
        # Fetch chat messages from db
        return await sync_to_async(ChatMessage.objects.all)()