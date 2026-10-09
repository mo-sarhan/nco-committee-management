from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.photos.models import PhotoType
from apps.users.serializers import UserSerializerBasic

from .models import (
    PhotoType,
    PhotoInfo,
    PhotoStatusType,
    RejectPhotoReason,
    RejectPhotoInfo,
)





class RejectPhotoReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectPhotoReason
        fields = '__all__'

class RejectPhotoSerializer(serializers.Serializer):
    photo_id = serializers.IntegerField(required=True)
    reject_code = serializers.IntegerField(required=True)
    reject_user_code = serializers.IntegerField(required=True)

class RejectPhotoInfoSerializer(serializers.ModelSerializer):
    reason = serializers.SerializerMethodField(read_only=True)
    # reject_code= RejectPhotoReasonSerializer(read_only=True)

    def get_reason(self,obj):
        reason = RejectPhotoReason.objects.filter(pk=obj.reject_code.pk)
        serializer = RejectPhotoReasonSerializer(reason,many=True)
        return serializer.data
    # reject_user_code = UserSerializerBasic(read_only=True,source = '')
    class Meta:
        model = RejectPhotoInfo
        fields = '__all__'
        read_only_fields = ['active_flag','delete_flag','reject_user_code','reject_user_date','reason']

class PhotoStatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoStatusType
        fields = '__all__'
        read_only_fields = ['active_flag','delete_flag']


class PhotoInfoSerializerBasic(serializers.ModelSerializer):
    class Meta:
        model = PhotoInfo
        fields = '__all__'

class PhotoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoType
        fields = '__all__'


class PhotoInfoSerializerBasic(serializers.ModelSerializer):
    class Meta:
        model = PhotoInfo
        fields = '__all__'
        read_only_fields = ['active_flag','delete_flag','photo_id']

class PhotoInfoSerializer(serializers.ModelSerializer):
    # photo_type = PhotoTypeSerializer(many=True,source = 'photo_info')
    photo_type=serializers.SerializerMethodField(read_only=True)
    # reject_reason = RejectPhotoInfoSerializer(many=True,source = 'rejected_history',read_only=True)
    reject_reason = serializers.SerializerMethodField(read_only=True)
    photo_status =  PhotoStatusTypeSerializer(read_only=True)

    def get_reject_reason(self,obj):
        queryset = obj.rejected_history.filter(active_flag=True,delete_flag=False)
        return RejectPhotoInfoSerializer(queryset,many=True).data

    def get_photo_type (self,obj):
        type_code = PhotoType.objects.filter(pk=obj.photo_type_code.photo_type_code)
        serializer = PhotoTypeSerializer(type_code,many=True)
        return serializer.data

    def create(self, validated_data):
        family=PhotoType.objects.filter(pk=3).first()
        if validated_data.get('photo_type_code') == family and validated_data.get('photo_family_serial',None) == None:
            raise ValidationError('you should set photo family serial with family photo')

        return super().create(validated_data)

    class Meta:
        model = PhotoInfo
        fields = '__all__'
        read_only_fields = ['photo_id','photo_person_degree_code','active_flag','delete_flag','photo_status','review_user','objects','custom_objects']
        ordering = ['photo_id','photo_type_code']


class UploadImageSerializer(serializers.Serializer):
    mil_ser = serializers.IntegerField(required=True)
    photo_path= serializers.ImageField(required=True)
    photo_family_serial = serializers.IntegerField(required=False)
    photo_type_code = serializers.IntegerField(required=True) 
    create_user = serializers.IntegerField(required=True)
    prnt_army_code = serializers.IntegerField(required=False)
