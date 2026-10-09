from django.db import transaction
from channels.layers import get_channel_layer
from apps.report.services.generate_photo_report import generate_photo_report
import datetime
from asgiref.sync import async_to_sync
from ..serializers import UploadImageSerializer
from ..models import (
    PhotoInfo,
    PhotoType,
    )

from ..serializers import PhotoInfoSerializerBasic,PhotoInfoSerializerBasic
from rest_framework import serializers

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
# @transaction.atomic
# def upload_photo(request):
#     try:

#         mil_ser = request.data.getlist('mil_ser')
#         photo_path = request.data.getlist('photo_path')
#         photo_type_code = request.data.getlist('photo_type_code')
#         photo_family_serial = request.data.getlist('photo_family_serial')
#         print(request.data)
#         for i in [mil_ser,photo_path,photo_type_code,photo_family_serial]:
#             print(len(i))
#         if not (len(mil_ser) == len(photo_path) == len(photo_type_code) == len(photo_family_serial)):
#             raise Exception("please correct the data and ")
        


#         photo_serializer = PhotoInfoSerializer(data=request.data, many=True)
#         photo_serializer.is_valid(raise_exception=True)
#         # Deactivate existing photos per entry
#         for photo_data in photo_serializer.validated_data:
#             photo_type = photo_data.get('photo_type_code')
#             family_serial = photo_data.get('photo_family_serial')
#             person = photo_data.get('mil_ser')

#             person.photos.filter(
#                 photo_type_code=photo_type.photo_type_code,
#                 photo_family_serial=family_serial
#             ).update(active_flag=False)

#         # Save new photos
#         photo_serializer.save(review_user=None,create_user=request.user)

#         return photo_serializer.data

#     except Exception as e:
#         raise Exception(str(e))
#         raise serializers.ValidationError({'error': str(e)})




@transaction.atomic
def upload_photo(request):
    try:
        photo_serializer = PhotoInfoSerializerBasic(data=request.data.copy())
        # print(request.data)
        photo_serializer.is_valid(raise_exception=True)
        # print(photo_serializer.validated_data)
        photo_type = photo_serializer.validated_data.get('photo_type_code')
        family_serial = photo_serializer.validated_data.get('photo_family_serial')
        if photo_type.photo_type_code != 3:
            family_serial = None
        person = photo_serializer.validated_data.get('mil_ser')
        # lock the mil_ser or (AfrPerson) so that many request can not create duplicated data in photo
        type(person).objects.select_for_update().get(pk=person.mil_ser)

        query=person.photos.filter(photo_type_code=photo_type.photo_type_code,photo_family_serial=family_serial)
        query.update(active_flag=False)
        photo_serializer.save(review_user=None,create_user=request.user)

        group_name=f'photo_report_{person.prnt_army_code}'
    

        # print('group_name',group_name)
        send_websocket_report(person.prnt_army_code,group_name)
        send_websocket_report(None,'photo_report')
        return PhotoInfoSerializerBasic(person.photos.filter(active_flag=True,delete_flag=False),many=True).data
    except Exception as e:
        raise Exception({'error':str(e)})
