from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,User
from apps.tanzem.models import ArmyCode,Rank,Jobs
from datetime import datetime
import os

# Create your models here.



def upload_profile_photo(obj,filename):
    name,ext = os.path.splitext(filename)
    new_name = f'{obj.user.username}{ext}'
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_path= os.path.join('profiles',str(obj.user.username),timestamp,new_name)
    return new_path

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=False,related_name='profile')
    mil_no = models.BigIntegerField(null=True,blank=True)
    # army_code = models.IntegerField(null=True,blank=True)
    # army_name = models.CharField(null=True,blank=True,max_length=255)
    # rank_code = models.IntegerField(null=True,blank=True)
    rank_code = models.ForeignKey(Rank,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='profile',db_column='RANK_CODE')
    rank_name = models.CharField(max_length=255,null=True,blank=True)
    # prnt_army_code = models.IntegerField(null=True,blank=True)
    # prnt_army_name = models.CharField(null=True,blank=True,max_length=255)
    job = models.ForeignKey(Jobs,on_delete=models.DO_NOTHING,null=True,blank=True,db_column='JOB')
    password = models.CharField(null=True,blank=True,max_length=255)
    profile_photo = models.ImageField(null=True,blank=True,upload_to=upload_profile_photo)
    
    army_code = models.ForeignKey(ArmyCode,to_field='army_code',on_delete=models.SET_NULL,null=True,blank=True,related_name='army_profile',db_column='ARMY_CODE')
    prnt_army_code = models.ForeignKey(ArmyCode,to_field='army_code',on_delete=models.SET_NULL,null=True,blank=True,related_name='prnt_profile',db_column='PRNT_ARMY_CODE')

    def __str__(self):
        return str(self.user) 
    # + self.prnt_army_code.army_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'USERS_PROFILE'
        ordering = ['user','army_code','prnt_army_code']




