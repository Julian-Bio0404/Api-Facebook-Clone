"""Chats consumers."""

# Utils
import json

# Channels
from asgiref.sync import async_to_sync, sync_to_async
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async

# Models
from app.users.models import User
from app.chats.models import Message, Thread


class ChatConsumer(AsyncConsumer):
    """Chat Consumer."""

    async def websocket_connect(self, event):
        user = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = await sync_to_async(User.objects.get)(username=other_username)

        self.thread = await sync_to_async(
            Thread.objects.get_or_create_personal_thread)(user, other_user)

        self.room_name = f'personal thread {self.thread.id}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.send({'type': 'websocket.accept'})
        print(f'[{self.channel_name}] - You are connected.')

    async def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')
        message = json.dumps(
            {'text': event.get('text'), 'username': self.scope['user'].username})
        
        await self.store_message(event.get('text'))

        await self.channel_layer.group_send(
            self.room_name, {'type': 'websocket.message', 'text': message})
        
    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message sent - {event["text"]}')
        await self.send({'type': 'websocket.send', 'text': event.get('text')})
    
    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] -Disconnected.')
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    @database_sync_to_async
    def store_message(self, text):
        """Create a message."""
        Message.objects.create(
            thread=self.thread, sender=self.scope['user'], text=text)


class EchoConsumer(SyncConsumer):
    """Consumer."""

    def websocket_connect(self, event):
        self.room_name = 'broadcast'
        self.send({'type': 'websocket.accept'})
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name)
        print(f'[{self.channel_name}] - You are connected.')

    def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {'type': 'websocket.message', 'text': event.get('text')})
        
    def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message sent - {event["text"]}')
        self.send({'type': 'websocket.send', 'text': event.get('text')})
    
    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] -Disconnected.')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name)
        print(event)
