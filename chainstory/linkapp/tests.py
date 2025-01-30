from django.test import TestCase, Client
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import reverse, re_path
from .consumers import ChatConsumer
from .models import ChatMessage, User
import json
from asgiref.sync import sync_to_async

class ChatConsumerTests(TestCase):
    async def test_connect(self):
        """Test that websocket can connect successfully"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            "/ws/chat/"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected, "WebSocket connection failed")
        await communicator.disconnect()

    async def test_send_message(self):
        """Test sending a chat message"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            "/ws/chat/"
        )
        await communicator.connect()
        
        # Send a test message
        await communicator.send_json_to({
            'type': 'message',
            'message': 'Hello, test!',
            'name': 'testuser',
            'color': '#000000'
        })

        # Receive response
        response = await communicator.receive_json_from()
        
        # Check response format
        self.assertEqual(response['message'], 'Hello, test!', "Message content does not match")
        self.assertEqual(response['color'], '#000000', "Message color does not match") 
        
        # Check database
        chat_message_count = await sync_to_async(ChatMessage.objects.count)()
        self.assertEqual(chat_message_count, 1, "ChatMessage count is not as expected")  
        user_count = await sync_to_async(User.objects.count)()
        self.assertEqual(user_count, 1, "User count is not as expected") 
        
        await communicator.disconnect()

    async def test_request_history(self):
        """Test requesting chat history"""
        # Create some test messages
        user = await sync_to_async(User.objects.create)(username='testuser', color='#000000')
        await sync_to_async(ChatMessage.objects.create)(user=user, content='Test message', color='#000000')
        
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            "/ws/chat/"
        )
        await communicator.connect()
        
        # Request history
        await communicator.send_json_to({
            'type': 'request_history'
        })
        
        # Check response
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'history', "Response type is not 'history'") 
        self.assertEqual(len(response['messages']), 1, "Number of messages in history is not as expected")  
        self.assertEqual(response['messages'][0]['content'], 'Test message', "Content of the first message does not match")  
        
        await communicator.disconnect()
