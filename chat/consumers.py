from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import get_user

import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'room_{self.room_id}'
        print(self.room_id, self.group_name, self.channel_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = await get_user(self.scope)
        print(user)  # user is AnonymousUser
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': 3,  # imitation
                'sender_name': "Lee",  # imitation
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['sender_id']
        user_name = event['sender_name']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': user_id,
            'sender_name': user_name,
        }))
