from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.models import ChatRoom, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']

            if not await self.check_room_exits(self.room_id):
                raise ValueError('채팅방이 존재하지 않습니다.')

            group_name = self.get_group_name(self.room_id)

            await self.channel_layer.group_add(group_name, self.channel_name)
            await self.accept()

        except ValueError as e:
            await self.send_json({'error': str(e)})
            await self.close()

    async def disconnect(self, close_code):
        try:
            group_name = self.get_group_name(self.room_id)
            await self.channel_layer.group_discard(group_name, self.channel_name)

        except Exception as e:
            pass

    async def receive_json(self, content, **kwargs):
        try:
            message = content['message']
            sender_email = content['sender_email']
            shop_user_email = content.get('shop_user_email')
            visitor_user_email = content.get('visitor_user_email')

            if not shop_user_email or not visitor_user_email:
                raise ValueError("상점 및 방문자 이메일이 모두 필요합니다")

            room = await self.get_or_create_room(shop_user_email, visitor_user_email)

            self.room_id = str(room.id)

            group_name = self.get_group_name(self.room_id)

            await self.save_message(room, sender_email, message)

            await self.channel_layer.group_send(group_name, {
                'type': 'chat_message',
                'message': message,
                'sender_email' : sender_email
            })

        except ValueError as e:
            await self.send_json({'error': str(e)})

    async def chat_message(self, event):
        try:
            message = event['message']
            sender_email = event['sender_email']

            await self.send_json({'message': message, 'sender_email': sender_email})

        except Exception as e:
            await self.send_json({'error': '메시지 전송 실패'})

    @staticmethod
    def get_group_name(room_id):
        return f"chat_room_{room_id}"

    @database_sync_to_async
    def get_or_create_room(self, shop_user_email, visitor_user_email):
        try:
            room = ChatRoom.objects.get(shop_user__shop_user_email=shop_user_email, visitor_user__visitor_user_email=visitor_user_email)
            return room
        except ChatRoom.DoesNotExist:
            raise ValueError("채팅방이 존재하지 않습니다.")

    @database_sync_to_async
    def save_message(self, room, sender_email, message_text):
        if not sender_email or not message_text:
            raise ValueError("발신자 이메일 및 메시지 텍스트가 필요합니다.")
        Message.objects.create(room=room, sender_email=sender_email, text=message_text)

    @database_sync_to_async
    def check_room_exits(self, room_id):
        return ChatRoom.objects.filter(id=room_id).exits()