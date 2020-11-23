import time

from django.test import TestCase
from channels.testing import WebsocketCommunicator

from asgiref.sync import sync_to_async

from account.models import Author
from chat.consumers import ContactConsumer, ChatRoomConsumer


# Create your tests here.
class ChatContactTest(TestCase):
    fixtures = ['users.json']

    async def test_u2u_chat(self):
        comm11 = WebsocketCommunicator(
            ContactConsumer.as_asgi(), '/ws/chat/')
        await self._set_user(comm11, pk=3)
        comm12 = WebsocketCommunicator(
            ContactConsumer.as_asgi(), '/ws/chat/')
        await self._set_user(comm12, pk=3)
        comm21 = WebsocketCommunicator(
            ContactConsumer.as_asgi(), '/ws/chat/')
        await self._set_user(comm21, pk=4)
        comm31 = WebsocketCommunicator(
            ContactConsumer.as_asgi(), '/ws/chat/')
        await self._set_user(comm31, pk=5)
        connected, subp = await comm11.connect()
        self.assertTrue(connected)
        connected, subp = await comm12.connect()
        self.assertTrue(connected)
        connected, subp = await comm21.connect()
        self.assertTrue(connected)
        connected, subp = await comm31.connect()
        self.assertTrue(connected)
        await comm11.send_json_to({
            'message': 'hello',
            'dest': "user_3_4",
        })
        res = await comm11.receive_json_from(timeout=60)
        expected_msg = {
            'message': 'hello',
            'sender_id': 3,
            'sender_name': 'test',
            'dest': 'user_3_4',
        }
        # message will send back to self to confirm
        self.assertEqual(res, expected_msg)
        # message will send to another self client to sync
        self.assertEqual(await comm12.receive_json_from(), expected_msg)
        # message will send to the dest user
        self.assertEqual(await comm21.receive_json_from(), expected_msg)
        # message wont send to an unrelevant user
        self.assertTrue(await comm31.receive_nothing())
        await comm11.disconnect()
        await comm12.disconnect()
        await comm21.disconnect()
        await comm31.disconnect()

    @sync_to_async
    def _set_user(self, comm, pk):
        u = Author.objects.get(pk=pk)
        name = u.username
        comm.scope['user'] = u


class ChatRoomTest(TestCase):
    fixtures = ['users.json']

    async def test_room_chat(self):
        comm11 = WebsocketCommunicator(
            ChatRoomConsumer.as_asgi(), '/ws/chat/1/')
        await self._set_user(comm11, pk=3)
        comm11.scope['url_route'] = {
            'kwargs': {
                'room_id': 1,
            }
        }
        comm21 = WebsocketCommunicator(
            ChatRoomConsumer.as_asgi(), '/ws/chat/1/')
        await self._set_user(comm21, pk=4)
        comm21.scope['url_route'] = {
            'kwargs': {
                'room_id': 1,
            }
        }
        comm31 = WebsocketCommunicator(
            ChatRoomConsumer.as_asgi(), '/ws/chat/2/')
        await self._set_user(comm31, pk=5)
        comm31.scope['url_route'] = {
            'kwargs': {
                'room_id': 2,
            }
        }
        connected, subp = await comm11.connect()
        self.assertTrue(connected)
        connected, subp = await comm21.connect()
        self.assertTrue(connected)
        connected, subp = await comm31.connect()
        self.assertTrue(connected)
        await comm11.send_json_to({
            'message': 'hello',
        })
        expected_msg = {
            'message': 'hello',
            'sender_id': 3,
            'sender_name': 'test',
        }
        # message will send back to self to confirm
        self.assertEqual(await comm11.receive_json_from(), expected_msg)
        # message will send to the other user in the same room
        self.assertEqual(await comm21.receive_json_from(), expected_msg)
        # message wont send to an unrelevant user
        self.assertTrue(await comm31.receive_nothing())
        await comm11.disconnect()
        await comm21.disconnect()
        await comm31.disconnect()

    @sync_to_async
    def _set_user(self, comm, pk):
        u = Author.objects.get(pk=pk)
        name = u.username
        comm.scope['user'] = u

    @sync_to_async
    def _user_login(self, username, pwd):
        self.client.login(username=username, password=pwd)
