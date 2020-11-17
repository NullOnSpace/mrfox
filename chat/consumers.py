from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import get_user

import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await get_user(self.scope)
        if not user.is_authenticated:
            await self.close()
        else:
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
        print(user)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'room_message',
                'message': message,
                'sender_id': user.id,
                'sender_name': user.username,
            }
        )

    async def room_message(self, event):
        message = event['message']
        user_id = event['sender_id']
        user_name = event['sender_name']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': user_id,
            'sender_name': user_name,
        }))


class ContactConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await get_user(self.scope)
        if not user.is_authenticated:
            await self.close()
        else:
            self.group_name = f'user_{user.id}'
            print(self.group_name, self.channel_name)
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
        dest = text_data_json['message']
        type_, pk = dest.split("_")
        pk = int(pk)
        user = await get_user(self.scope)
        # send to selfs
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': user.id,
                'sender_name': user.username,
                'dest': dest,
                'exclude': self.channel_name,
            }
        )
        if type_ == "user":
            dest_group_name = f"user_{pk}"
            await self.channel_layer.group_send(
                dest_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'sender_id': user.id,
                    'sender_name': user.username,
                    'dest': dest,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        dest = event['dest']
        user_id = event['sender_id']
        user_name = event['sender_name']
        exclude = event['exclude']
        if self.channel_name != exclude:
            await self.send(text_data=json.dumps({
                'message': message,
                'sender_id': user_id,
                'sender_name': user_name,
                'dest': dest,
            }))
