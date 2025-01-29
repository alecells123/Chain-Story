from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the chat group
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()
        
        # Get messages using sync_to_async
        from .models import ChatMessage, User  # Import here to avoid circular import
        get_messages = sync_to_async(lambda: list(ChatMessage.objects.all()))
        messages = await get_messages()
        

    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        from .models import ChatMessage, User
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']
        color = text_data_json.get('color', '#000000')

        # Get or create user
        get_or_create_user = sync_to_async(User.objects.get_or_create)
        user, created = await get_or_create_user(username=name, defaults={'color': color})
        
        if not created and user.color != color:
            # Update user's color if it changed
            user.color = color
            save_user = sync_to_async(lambda u: u.save())
            await save_user(user)

        # Save message
        save_message = sync_to_async(ChatMessage.objects.create)
        await save_message(content=message, user=user, color=color)

        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat_message",
                "message": message,
                "name": name,
                "color": color
            }
        )

    async def chat_message(self, event):
        message = event['message']
        name = event['name']
        color = event['color']
        await self.send(text_data=json.dumps({
            'message': message,
            'name': name,
            'color': color
        }))

    async def get_chat_messages(self):
        # Fetch chat messages from db
        return await sync_to_async(ChatMessage.objects.all)()