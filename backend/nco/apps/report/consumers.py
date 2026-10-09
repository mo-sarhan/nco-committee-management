from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.report.services.generate_photo_report import generate_photo_report
import json

class PrntPhotoReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close(code=4001)
            return

        self.groups_names = await self.get_group_name()
        # print('()'*3,self.groups_names)
        for group in self.groups_names:
            # print('group',group)

            await self.channel_layer.group_add(
                group,
                self.channel_name
            )

        await self.accept()
        await self.send(text_data=await self.get_report())

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        if hasattr(self, "groups_names"):
            for group in self.groups_names:
                await self.channel_layer.group_discard(
                    group,
                    self.channel_name
                )

    @database_sync_to_async
    def get_group_name(self):
        try:
            groups_name = []
            if self.user.is_superuser or self.user.has_perm('report.can_see_all_army'):
                groups_name.append('photo_report')
            else:
                groups_name.append(f'photo_report_{self.user.profile.prnt_army_code_id}')

            # print('*#'*3,groups_name)
            return groups_name
        except Exception as e:
            # print('exception',str(e))
            return []

    @database_sync_to_async
    def get_report(self):
        prnt_army_code = self.user.profile.prnt_army_code_id
        if self.user.is_superuser or self.user.has_perm('report.can_see_all_army'):
            prnt_army_code = None

        return generate_photo_report(prnt_army_code)

    # @database_sync_to_async
    # def get_report(self):
    #     prnt_army_code = self.user.profile.prnt_army_code_id



    # Server → Client only
    async def report_update(self, event):
        await self.send(text_data=event["data"])



