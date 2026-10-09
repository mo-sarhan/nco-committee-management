from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.person.models import AfrPerson,AfrDegree
from datetime import datetime
import os

# Create your models here.

class PhotoType(models.Model):
    photo_type_code = models.IntegerField(primary_key=True,null=False)
    photo_type_name = models.CharField(max_length=500,null=False)
    delete_flag = models.BooleanField(default=False)
    active_flag = models.BooleanField(default=True)

    def __str__(self):
        return self.photo_type_name

    def delete(self, *args,**kwargs):
        """ soft delete """
        self.delete_flag=True
        self.active_flag=False
        self.save()

    def hard_delete(self,*args,**kwargs):
        """delete the record from database"""
        return super().delete(*args,**kwargs)



    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'PHOTO_TYPE'


def upload_to(obj,filename):
    name,ext = os.path.splitext(filename)
    new_name = f'{obj.mil_ser.mil_no}_{obj.mil_ser.degree_code_id}_{obj.photo_type_code.photo_type_code}_{obj.photo_family_serial or ''}{ext}'
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_path= os.path.join(str(obj.mil_ser.army_code).replace(' ','_'),str(obj.mil_ser.mil_no),timestamp,new_name)
    return new_path

# def validate_photo(obj):
#     name,ext = os.path.splitext(obj)
#     if not (ext.tolower() in ['jpg','png','jpeg'] )


class CustomPhotoQuery(models.QuerySet):

    def get_active_photos(self):
        return self.filter(delete_flag=False,active_flag=True)
    

    def get_unactive_photos(self):
        return self.filter(active_flag=False)
        

class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomPhotoQuery(self.model,using=self._db)
    
    def  get_active_photos(self):
        return self.get_queryset().get_active_photos()

    def get_unactive_photos(self):
        return self.get_queryset().get_unactive_photos()
    

class PhotoStatusType(models.Model):
    status_code = models.IntegerField(primary_key=True,null=False,db_column='STATUS_CODE')
    status_name = models.CharField(max_length=255,null=False,blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active_flag = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.status_name

    def delete(self,*args,**kwargs):
        self.delete_flag = True
        self.active_flag = False
        self.save()

    def hard_delete(self,*args,**kwargs):
        return super().delete(args,kwargs)
    

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'PHOTO_STATUS_TYPE'
        ordering = ['status_code']
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['status_code','status_name'],
        #         name="photo_status_type_status_code_status_name",
        #     )
        # ]
        
    
def family_serial_validator(value):
    # print('*'*50,value)
    if not (value   in [None,1,2,3,4]):
        raise ValidationError(f'family serial {value} must be in range [1-4]')

class PhotoInfo(models.Model):
    photo_id = models.BigAutoField(primary_key=True,null=False)
    mil_ser  = models.ForeignKey(AfrPerson,on_delete=models.DO_NOTHING,null=False,related_name='photos',db_column='MIL_SER')
    photo_type_code = models.ForeignKey(PhotoType,on_delete=models.DO_NOTHING,related_name='photo_info',db_column='PHOTO_TYPE_CODE',null=False)
    create_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='photo_info',db_column='CREATE_USER')

    is_nsfw = models.BooleanField(null=True,blank=True)

    photo_person_degree_code = models.ForeignKey(AfrDegree,on_delete=models.DO_NOTHING,null=True,blank=True,db_column='PHOTO_PERSON_DEGREE_CODE')
    photo_path = models.ImageField(upload_to=upload_to,null=True,blank=True,max_length=500)
    photo_family_serial = models.IntegerField(null=True,blank=True,validators=[family_serial_validator])
    create_date = models.DateTimeField(auto_now_add=True)

    review_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='review_photo',db_column='REVIEW_USER')
    review_date = models.DateTimeField(null=True,blank=True)

    active_flag = models.BooleanField(default=True)
    photo_status = models.ForeignKey(PhotoStatusType,on_delete=models.SET_NULL,null=True,default=0,related_name='photo_info',db_column='PHOTO_STATUS')
    delete_flag=models.BooleanField(default=False)

    objects = models.Manager()
    custom_objects = CustomManager()

    def clean(self):
        # print('*'*10,self.photo_type_code)
        if self.photo_type_code.photo_type_code ==  3 and self.photo_family_serial == None:
            raise ValidationError(f"photo_family_serial must be set with {self.photo_type_code}")
        if not (self.photo_family_serial in [None,1,2,3,4]):
            raise ValidationError(f"photo family serial must be in range [1-4]")

    def delete(self,*args,**kwargs):
        """ soft delete just set delete flag true"""
        self.delete_flag=True
        self.active_flag=False
        self.save()

    def hard_delete(self,*args,**kwargs):
        """ delete from database"""
        return super().delete(*args,**kwargs)
    
    def save(self,*args,**kwargs):
        self.full_clean()
        self.photo_person_degree_code = self.mil_ser.degree_code
        # print(self.photo_family_serial)
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return  f'{self.mil_ser.person_name}-{self.photo_type_code.photo_type_name}'
    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table='PHOTO_INFO'
        ordering = ['mil_ser','-active_flag','photo_type_code','photo_family_serial']
        permissions = [
            ('can_reject_photo','can reject photo'),
        ]
        # constraints = [
        #     models.UniqueConstraint(
        #         # fields=['mil_ser','photo_type_code','photo_person_degree_code','active_flag'],
        #         fields=['mil_ser','photo_type_code','active_flag'],
        #         name="unique_mil_ser__type__degree,active",
        #     )
        # ]



class RejectPhotoReason(models.Model):
    reject_code = models.IntegerField(primary_key=True,null=False,blank=False,unique=True)
    reject_name = models.CharField(null=False,blank=False,max_length=500,unique=True)
    active_flag = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)

    def delete(self, using = ..., keep_parents = ...):
        self.delete_flag=True
        self.active_flag=False
        self.save()

    def hard_delete(self, using = ..., keep_parents = ...):
        return super().delete(using, keep_parents)

    def __str__(self):
        return self.reject_name
    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'PHOTO_REJECT_CODE'


class RejectPhotoInfo(models.Model):
    photo_reject_id = models.BigAutoField(primary_key=True,blank=False,null=False)
    photo_id = models.ForeignKey(PhotoInfo,on_delete=models.DO_NOTHING,null=False,related_name='rejected_history',db_column='PHOTO_ID')
    reject_code = models.ForeignKey(RejectPhotoReason,on_delete=models.DO_NOTHING,null=False,related_name='rejected_photos',db_column='REJECT_CODE')

    reject_user_code = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,related_name='rejected_photos',db_column='REJECT_USER_CODE')
    reject_user_date = models.DateTimeField(auto_now_add=True)

    update_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='updated_rejected_photos',db_column='UPDATE_USER')
    update_date = models.DateTimeField(auto_now=True)

    reject_note = models.CharField(max_length=500,null=True,blank=True)
    active_flag = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)

    def delete(self, *args,**kwargs):
        self.delete_flag=True
        self.active_flag=False
        self.save(update_fields=['active_flag','delete_flag'])

    def hard_delete(self, *args,**kwargs):
        return super().delete(*args,**kwargs)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'PHOTO_REJECT_INFO'

        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['photo_id','reject_code','reject_user_code'],
        #         name='reject_photo_constraints',
        #     )
        # ]
        


