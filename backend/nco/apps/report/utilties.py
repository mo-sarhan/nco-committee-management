
from channels.layers import get_channel_layer
# from .services import generate_photo_report
from .services.generate_photo_report import generate_photo_report
from asgiref.sync import async_to_sync
import datetime


def send_websocket_report(prnt_army_code,group):
    channel_layer = get_channel_layer()
    data = generate_photo_report(prnt_army_code)
    async_to_sync(channel_layer.group_send)(
        group,
        {
            "type": "report_update",
            "message": datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
            "data": data,
        }
    )