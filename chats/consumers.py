import asyncio
import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chats.models import ChatRoom, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    room_id = None

    async def connect(self):
        # websocket 연결 시
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']

            if not await self.check_room_exists(self.room_id):
                raise ValueError('Non-existent chat room')

            group_name = self.get_group_name(self.room_id)

            await self.channel_layer.group_add(group_name, self.channel_name)
            await self.accept() # websocket 연결 수락
            self.ping_task = asyncio.create_task(self.send_ping())

        except ValueError as e:
            await self.send_json({'error': str(e)})
            await self.close()

    async def disconnect(self, close_code):
        # websocket 연결 종료 시
        try:
            group_name = self.get_group_name(self.room_id)
            await self.channel_layer.group_discard(group_name, self.channel_name)
            self.ping_task.cancel()
        except Exception as e:
            await self.send_json({'error': str(e)})

    async def send_ping(self):
        while True:
            await asyncio.sleep(10)  # 10초마다 핑 메시지를 보냄
            await self.send(text_data=json.dumps({
                'type': 'ping',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }))

    async def receive_json(self, content, **kwargs):
        try:
            message = content['message']
            sender_email = content['sender_email']
            shop_user_email = content['shop_user_email']
            visitor_user_email = content['visitor_user_email']

            room = await self.get_or_create_room(shop_user_email, visitor_user_email)
            self.room_id = str(room.id)
            group_name = self.get_group_name(self.room_id)

            await self.save_message(room, sender_email, message)
            # from datetime import datetime
            data = {
                'type': 'chat_message',
                'message': message,
                'sender_email': sender_email,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            await self.channel_layer.group_send(group_name, data)

        except KeyError as e:
            await self.send_json({'error': f'{str(e)} is required'})

    async def chat_message(self, event):
        try:
            message = event['message']
            sender_email = event['sender_email']
            timestamp = event['timestamp']

            message = {
                'message': message,
                'sender_email': sender_email,
                'timestamp': timestamp
            }
            await self.send_json(message)

        except KeyError as e:
            await self.send_json({'error': f'{str(e)} is required'})

    @staticmethod
    def get_group_name(room_id):
        return f'chat_room_{room_id}'

    @database_sync_to_async
    def get_or_create_room(self, shop_user_email, visitor_user_email):
        try:
            room = ChatRoom.objects.get(
                shop_user__shop_user_email=shop_user_email,
                visitor_user__visitor_user_email=visitor_user_email
            )
        except ChatRoom.DoesNotExist:
            raise ValueError('Non-existent chat room')
        return room

    @database_sync_to_async
    def save_message(self, room, sender_email, message_text):
        Message.objects.create(room=room, sender_email=sender_email, text=message_text)

    @database_sync_to_async
    def check_room_exists(self, room_id):
        return ChatRoom.objects.filter(id=room_id).exists()