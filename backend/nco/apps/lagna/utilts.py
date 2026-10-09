from channels.layers import get_channel_layer
import datetime
from asgiref.sync import async_to_sync



#-------------------------------

def send_websocket_data(data,group,type):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group,
        {
            "type": type,
            "message": datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
            "data": data,
            "event":type
        }
    )



def get_web_socket_group(lagna_code,member_type):
    return [
        f'comm_{lagna_code}',
        f'comm_{lagna_code}_{member_type}'
    ]