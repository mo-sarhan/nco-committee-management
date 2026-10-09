
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.report.services.generate_photo_report import generate_photo_report
from django.core.cache import cache
from urllib.parse import parse_qs
import json

class LagnaShowConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            user = self.scope["user"]
            self.lagna_member = None
            self.cache_lagna_key = None

            if user.is_anonymous:
                await self.close(code=4001)
                return

            print(await self.get_lagna())
            self.lagna_code,self.member_type =await self.get_lagna()
            self.groups = []
            self.groups.append( f"comm_{self.lagna_code}")
            self.groups.append(f"comm_{self.lagna_code}_{self.member_type}")

            for group in self.groups:
                await self.channel_layer.group_add(
                    group,
                    self.channel_name
                )

            await self.accept()
            await self.send_settings()
            cache_lagna_key = f'comm_{self.lagna_code}'
            self.cache_lagna_key = cache_lagna_key
            cache_data = cache.get(cache_lagna_key)
            if cache_data:
                await self.send(text_data=cache_data)
        except Exception as e:
            print(e)
            self.close()


    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    @database_sync_to_async
    def get_lagna(self):
        try:
            query_string = self.scope.get("query_string", b"").decode()
            params = parse_qs(query_string)
            user = self.scope['user']
            lagna_code = params.get('lagna',[None])[0]
            print('super_user',user.is_superuser)
            # if user.is_superuser:
            #     return (lagna_code,'head')
            member = user.lagna_member.filter(committe_code__committe_code = lagna_code).first()
            if not member:
                if user.is_superuser:
                    return (lagna_code,'head')
                return ()

            self.lagna_member = member
            print('lagna member ',self.lagna_member)
            print('member',member)
            member_type = 'head' if member.member_type.member_type_code == 1 else 'voter'
            return (lagna_code,member_type)
        except Exception as e:
            print('error ',e)
            self.close()


    async def send_settings(self,event=None):
        try:
            settings = {
                'socket_group':None,
                'open_final_decision':False
            }

            if self.lagna_member:
                settings['socket_group'] = self.lagna_member.member_type.socket_group
                settings['open_final_decision'] = self.lagna_member.member_type.open_final_decision
            print('#'*5,' ',self.lagna_member)
            await self.send(text_data=json.dumps({
                'event':'settings',
                'settings':settings}
                ))
        except Exception as e:
            print('settings error',e)
            await self.close()

    # Server → Client only
    async def show_person(self, event):
        await self.send(text_data=event["data"])

    async def send_votes(self, event):
        await self.send(text_data=event["data"])

    async def show_comm_report(self, event):
        await self.send(text_data=event["data"])

    async def notify(self, event):
        message = event['message']
        data = event['data']
        await self.send(text_data=json.dumps({
            'message': message ,
            'data': data,
            'event': data
    }))
