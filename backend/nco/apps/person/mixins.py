from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from apps.photos.serializers import PhotoInfoSerializerBasic,PhotoInfoSerializer,RejectPhotoInfoSerializer
from apps.photos.models import PhotoStatusType,PhotoInfo
from apps.photos.permissions import HasPermToRejectPhoto
from .serializers import (
    AfrUnitsSerializer,
    AfrPsychologigcalReportSerializer,
    AfrSecuritySituationSerializer,
)



class AfrPersonUnitMixin:
    
    @transaction.atomic
    @action(detail=True,methods=['get'],url_path='units(?:/(?P<unit_code>\d+))?')
    def afr_person_units(self,request,pk=None,unit_code=None):
        try:
            # print('*'*10)
            person = self.get_object()
            # print('here','person')
            units = person.units.all()
            # print(units)
            # print('*'*5,unit_code)
            if unit_code:
                unit = units.get(unit_code=unit_code)
                serializer = AfrUnitsSerializer(unit)
                return Response(serializer.data,status=status.HTTP_200_OK)
            
            serializer = AfrUnitsSerializer(units,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error':str(e)},status=status.HTTP_200_OK)


class AfrPersonPhotosMixin:

    @transaction.atomic
    @action(detail=True,methods=['get'],url_path='photos(?:/(?P<photo_id>\d+))?')
    def afr_person_photo(self,request,pk=None,photo_id=None):
        try:
            person = self.get_object()
            photos = person.photos.filter(active_flag=True,delete_flag=False)
            if photo_id:
                photo = photos.get(pk=photo_id)
                serializer =PhotoInfoSerializer(photo)
                return Response(serializer.data,status=status.HTTP_200_OK)

            serializer = PhotoInfoSerializerBasic(photos,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error':str(e)})

    @transaction.atomic
    @action(detail=True,methods=['post'],permission_classes=[HasPermToRejectPhoto],url_path='photos/(?P<photo_id>\d+)/check')
    def afr_person_photo_check(self,request,pk=None,photo_id=None):
        try:

            person = self.get_object()
            photo = person.photos.get(pk=photo_id,active_flag=True,delete_flag=False)
            #--------------------------------------------------------------

            data=request.data.copy()
            # data['reject_user_code'] = request.user.pk
            accept  = bool(int(data.pop('accept',[0])[0]))
            if accept:          # for acceptable photo
                photo.photo_status = PhotoStatusType.objects.get(pk=1)      # this photo is acceptable
                photo.review_user = request.user
                photo.review_date = timezone.now()
                photo.save(update_fields = ['photo_status','review_user','review_date'])
                return Response({'ok':'accepted'},status=status.HTTP_200_OK)
            else:           # for acceptqable photo
                # ------------------------------------
                data['photo_id'] = photo.pk
                reject_serializer = RejectPhotoInfoSerializer(data=data)
                reject_serializer.is_valid(raise_exception=True)
                # photo= reject_serializer.validated_data.get('photo_id')
                # photo.rejected_history.update(active_flag=False,delete_flag=True)            # set all rejected reason active_flag field to False
                reject_serializer.save(reject_user_code=self.request.user)
                photo.review_user = self.request.user
                photo.review_date = timezone.now()
                photo.photo_status = PhotoStatusType.objects.get(pk=2)   # this photo is rejected
                photo.save(update_fields = ['photo_status','review_user','review_date'])
                return Response(reject_serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)



class AfrPsychologicalReportMixin:

    @transaction.atomic
    @action(detail=True,methods=['get'],url_path='psychologic(?:/(?P<psychologic_id>\d+))?')
    def get_psychologic(self,request,pk=None,psychologic_id=None):
        try:
            person = self.get_object()
            psychologic_reports = person.psycholgical_report.filter(active_flag=True,delete_flag=False)
            serializer = None
            if psychologic_id:
                psychologic = psychologic_reports.filter(pk=psychologic_id).first()
                serializer =AfrPsychologigcalReportSerializer(psychologic)
            serializer =AfrPsychologigcalReportSerializer(psychologic_reports,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            raise ValidationError(str(e))

    @transaction.atomic
    @action(detail=True,methods=['post'],url_path='psychologic/add')
    def add_psychologic(self,request,pk=None,psychologic_id=None):
        try:
            person = self.get_object()
            data = self.request.data.copy()
            data['mil_ser'] = person.mil_ser
            serializer = AfrPsychologigcalReportSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(create_user=self.request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(str(e))


    @transaction.atomic
    @action(detail=True,methods=['delete'],url_path='psychologic/(?P<psychologic_id>\d+)/delete')
    def delete_psychologic(self,request,pk=None,psychologic_id=None):
        try:
            person = self.get_object()
            psychologic_report = person.psycholgical_report.filter(pk=psychologic_id,active_flag=True,delete_flag=False).first()
            psychologic_report.active_flag=False
            psychologic_report.delete_flag=False
            psychologic_report.delete_user = self.request.user
            psychologic_report.delete_date = timezone.now()
            psychologic_report.save(update_fields = ['active_flag','delete_flag','delete_user','delete_date'])
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError(str(e))


class AfrSecurityMixin:
    @transaction.atomic
    @action(detail=True,methods=['get','post'],url_path='security(?:/(?P<security_id>\d+))?')
    def manipulate_security(self,request,pk=None,security_id=None):
        try:
            mil_ser = self.get_object()
            if self.request.method == 'GET':
                security = mil_ser.security.all()
                if security_id:
                    sec_data = security.get(pk=security_id)
                    serializer = AfrSecuritySituationSerializer(sec_data)
                    return Response(serializer.data)
                serializer = AfrSecuritySituationSerializer(security,many=True)
                return Response(serializer.data)
            elif self.request.method == 'POST':
                data = self.request.data.copy()
                data['mil_ser'] = mil_ser.mil_ser
                serializer = AfrSecuritySituationSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(create_user=self.request.user)
                return Response(serializer.data)

        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    # /(?P<psychologic_id>\d+)/
    @action(detail=True,methods=['get','post'],url_path='security/(?P<security_id>\d+)/delete')
    def delete_security(self,request,pk=None,security_id=None):
        try:
            afr_person = self.get_object()
            security = afr_person.security.all()
            sec_item = security.get(pk=security_id)
            sec_item.active_flag=False
            sec_item.delete_flag = True
            sec_item.delete_user = self.request.user
            sec_item.delete_date = timezone.now()
            sec_item.save(update_fields = ['active_flag','delete_flag','delete_user','delete_date'])
            return Response('deleted')
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
