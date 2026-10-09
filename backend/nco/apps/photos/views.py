from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from apps.person.models import AfrPerson
from .services.upload_image_services import upload_photo
from apps.photos.models import (
    RejectPhotoReason,
    PhotoStatusType,
    RejectPhotoInfo,
    PhotoInfo,
    PhotoType
    )
from apps.photos.serializers import (
    RejectPhotoReasonSerializer,
    RejectPhotoInfoSerializer,
    RejectPhotoSerializer,
    PhotoTypeSerializer

)
import json


# Create your views here.


class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    http_method_names = ['get','post']

    def get(self,request):
        try:
            query = PhotoType.objects.all()
            serializer = PhotoTypeSerializer(query,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            photo_info = upload_photo(request)
            return Response(photo_info,status=status.HTTP_201_CREATED)
        except Exception as e:
            # print(e)
            return Response({'error':f'{e}'},status=status.HTTP_400_BAD_REQUEST)

        

class RejectImageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        query= RejectPhotoReason.objects.filter(delete_flag=False,active_flag=True)
        serializer = RejectPhotoReasonSerializer(query,many=True)
        return Response(serializer.data)


    def post(self,request):
        try:
            data=request.data.copy()
            data['reject_user_code'] = request.user.pk
            accept  = bool(int(data.pop('accept',[0])[0]))

            if not accept:          # for reject photo
                reject_serializer = RejectPhotoInfoSerializer(data=data)
                if reject_serializer.is_valid(raise_exception=True):
                    photo_id = reject_serializer.validated_data.get('photo_id')
                    reject_serializer.save(review_date=timezone.now())
                    photo_id.photo_status = PhotoStatusType.objects.get(pk=2)   # this photo is rejected
                    photo_id.save(update_fields = ['photo_status'])
            else:           # for acceptqable photo
                pk = int(data['photo_id'])
                photo = PhotoInfo.objects.filter(pk=pk,active_flag=True,delete_flag=False).first()
                photo.photo_status = PhotoStatusType.objects.get(pk=1)      # this photo is acceptable
                photo.rejected_history.update(active_flag=False)            # set all rejected reason active_flag field to False
                photo.review_user = request.user
                photo.review_date = timezone.now()
                photo.save(update_fields = ['photo_status','review_user','review_date'])
            
            # send_websocket_report()
            return Response({'ok':'ok'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

        



            
            

        


