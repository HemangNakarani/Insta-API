from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("someone Arrived")
        user = self.scope['user']
        print(user)
        if user.is_anonymous:
            await self.close()
        else:
            self.room_name = user.username
            self.room_group_name = 'webchat_%s' % self.room_name
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, code):
        print("Some One Disconnected")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await super().disconnect(code)

    async def receive_json(self, content, **kwargs):
        print(content)
        room_name = content.get('room')
        await self.channel_layer.group_send(group=room_name, message=content)
        await self.echo_message(content)

    async def echo_message(self, message):
        print(self.room_group_name)
        await self.send_json(message)
