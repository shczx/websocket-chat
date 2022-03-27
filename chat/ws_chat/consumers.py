import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "chat"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_id = data['message_id']
        message = data['message']
        username = data['username']
        msg_type = data['message_type']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message_type': msg_type,
                'message_id': message_id,
                'message': message,
                'username': username
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        message_id = event['message_id']
        msg_type = event['message_type']

        await self.send(text_data=json.dumps({
            'message_type': msg_type,
            'message_id': message_id,
            'message': message,
            'username': username,
        }))


