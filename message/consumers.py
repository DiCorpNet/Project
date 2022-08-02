import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.templatetags.static import static

from .models import MessageDialog, MessageRoom


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close(404)

        self.group_room_name = self.scope['url_route']['kwargs']['room']

        if not self.access_room():
            await self.close(404)

        await self.channel_layer.group_add(
            self.group_room_name,
            self.channel_name
        )

        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        text = json.loads(text_data)
        type = text['type']

        if type == 'open':
            await self.channel_layer.group_send(
                self.group_room_name,
                {'type': 'channel_open',}
            )
        else:
            message = text['message']
            data = await self.new_message(message)
            if data.user.image:
                res = data.user.image.url
            else:
                res = static('images/users/avatar-2.jpg')
                await self.channel_layer.group_send(
                    self.group_room_name,
                    {
                        'type': 'chat_message',
                        'user': data.user.username,
                        'user_in': self.scope['user'].username,
                        'user_image': res,
                        'text': data.text,
                        'created': data.created.strftime("%H:%M"),
                        'id': data.id
                    }
                )

    async def channel_open(self, event):
        message = await self.channel_open_data(self.group_room_name)
        user = await self.user_to(self.group_room_name)
        await self.send(text_data=json.dumps({
            'type': 'open',
            'data': message,
            'userTo': user
        }))

    @database_sync_to_async
    def user_to(self, room):
        resource = MessageRoom.objects.get(layer=room)
        user = list()
        for item in resource.user.all().exclude(id=self.scope['user'].id):
            if item.image:
                image = item.image.url
            else:
                image = static('images/users/avatar-2.jpg')
            res = {'username': item.username, 'email': item.email, 'image': image, 'location': item.location.name,
                   'country': item.country.name, 'lang': item.language}
            user.append(res)
        return user

    @database_sync_to_async
    def channel_open_data(self, room):
        result = MessageDialog.objects.filter(layer__layer=room).order_by('-created')[:15]
        message = list()

        for item in result:
            if item.user.image:
                res = {'user': item.user.username, 'user_in': self.scope['user'].username, 'user_image': item.user.image.url,
                       'text': item.text, "id": item.id, 'created': item.created.strftime("%H:%M")}
            else:
                res = {'user': item.user.username, 'user_in': self.scope['user'].username,
                       'user_image': static('images/users/avatar-2.jpg'), 'text': item.text, "id": item.id,
                       'created': item.created.strftime("%H:%M")}
            message.append(res)
        return message





    @database_sync_to_async
    def new_message(self, message):
        room = MessageRoom.objects.get(layer=self.group_room_name)
        result = MessageDialog.objects.create(user=self.scope['user'], layer=room, text=message)
        return result

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['text'],
            'user': event['user'],
            'user_in': event['user_in'],
            'user_image': event['user_image'],
            'created': event['created'],
            'id': event['id']
        }))

    async def disconnect(self, code):
        pass

    @database_sync_to_async
    def access_room(self):
        return MessageRoom.objects.filter(user__in=[self.scope['user'].id], layer=self.group_room_name)
