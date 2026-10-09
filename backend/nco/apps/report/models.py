from django.db import models
from django.conf import settings
from apps.person.models import AfrPerson
from apps.tanzem.models import ArmyCode
from apps.lagna.models import (
    LagnaTypeSpacific,
    Lagna,
    LagnaVoteOpinoin,
    OpinionType,
)





class PrntPhotoReport(models.Model):
    st_id = models.IntegerField(null=True,blank=True)
    prnt_army_code = models.CharField(primary_key=True,max_length=4)
    prnt_army_name = models.CharField(max_length=255,null=True,blank=True)
    total = models.IntegerField(null=True,blank=True)
    completed = models.IntegerField(null=True,blank=True,db_column='S_COM')
    un_completed= models.IntegerField(null=True,blank=True,db_column='NO_S_COM')
    checked= models.IntegerField(null=True,blank=True,db_column='S_CHE')
    un_checked= models.IntegerField(null=True,blank=True,db_column='NO_S_CHE')
    approved = models.IntegerField(null=True,blank=True,db_column='S_APPROV')
    not_approved = models.IntegerField(null=True,blank=True,db_column='NO_S_APPROV')
    rest = models.IntegerField(null=True,blank=True,db_column='NEED')

    def __str__(self):
        return self.prnt_army_name



    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'V_PER_PHOTO_ST_PRNT'
        ordering = ['prnt_army_code']
        permissions = [
            ('can_see_all_army','can see all army'),
        ]



class UnitPhotoReport(models.Model):
    st_id = models.IntegerField(null=True,blank=True,db_column='ST_ID')
    prnt_army_code = models.CharField(null=True,blank=True,max_length=4)
    prnt_army_name	= models.CharField(null=True,blank=True,max_length=255)
    unit_code = models.CharField(max_length=200,primary_key=True)
    unit_name = models.CharField(null=True,blank=True,max_length=255)
    total = models.IntegerField(null=True,blank=True)
    completed = models.IntegerField(null=True,blank=True,db_column='S_COM')
    un_completed = models.IntegerField(null=True,blank=True,db_column='NO_S_COM')
    checked = models.IntegerField(null=True,blank=True,db_column='S_CHE')
    un_checked = models.IntegerField(null=True,blank=True,db_column='NO_S_CHE')
    approved = models.IntegerField(null=True,blank=True,db_column='S_APPROV')
    not_approved = models.IntegerField(null=True,blank=True,db_column='NO_S_APPROV')
    rest =  models.IntegerField(null=True,blank=True,db_column='NEED')

    def __str__(self):
        return self.unit_name


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'V_PER_PHOTO_ST_UNIT'
        ordering = ['prnt_army_code','unit_code']


class AfrPhotoActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_flag=True,delete_flag=False)

class AfrPhotoReport(models.Model):
    ph_id = models.IntegerField(null=False,blank=False)
    mil_ser = models.OneToOneField(AfrPerson,on_delete=models.DO_NOTHING,related_name='photo_report',primary_key=True,db_column='MIL_SER')
    completed_flag = models.BooleanField(null=True,blank=True,db_column='COMPLETE_FLAG')
    checked_flag = models.BooleanField(null=False,blank=False,db_column='CHECK_FLAG')
    approved_flag = models.BooleanField(null=False,blank=False,db_column='APPROVE_FLAG')
    update_date = models.DateTimeField(auto_now=True)
    active_flag = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)
    lock_half = models.BooleanField(null=False,blank=False)
    lock_tall = models.BooleanField(null=False,blank=False)
    lock_family	= models.BooleanField(null=False,blank=False)

    objects = AfrPhotoActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return str(self.mil_ser)

    def delete(self,*args,**kwargs):
        self.active_flag = False
        self.delete_flag = True
        self.save()


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_PHOTO_CH_INOF'
        ordering = ['mil_ser']


class LagnaAfrReport(models.Model):
    cps_id = models.BigAutoField(primary_key=True,null=False,db_column='CPS_ID')
    committe_code = models.IntegerField(null=True,blank=True,db_column='COMMITTE_CODE',verbose_name='كود اللجنة')
    committe_name = models.CharField(max_length=1000,null=True,blank=True,db_column='COMMITTE_NAME',verbose_name='اسم اللجنة')
    prnt_army_name = models.CharField(max_length=100,null=True,blank=True,db_column='PRNT_ARMY_NAME',verbose_name='تبعية اللجنة')
    prnt_army_code = models.CharField(max_length=4,null=True,blank=True,db_column='PRNT_ARMY_CODE',verbose_name='كود التبعية')
    spacific_code = models.ForeignKey(LagnaTypeSpacific,on_delete=models.DO_NOTHING,related_name='lagna_afr_report',null=True,blank=True,db_column='COMM_DA_TYPE_ID',verbose_name='كود اللجنة المخصصة')
    # spacific_code = models.IntegerField(null=True,blank=True,db_column='COMM_DA_TYPE_ID',verbose_name='كود اللجنة المخصصة')
    type_code = models.IntegerField(null=True,blank=True,db_column='COMMITTE_TYPE',verbose_name='كود نوع اللجنة')
    type_name = models.CharField(max_length=100,null=True,blank=True,db_column='TYPE_NAME',verbose_name='نوع اللجنة')
    person_prnt_army_code = models.CharField(max_length=4,null=True,blank=True,db_column='PERSON_PRNT',verbose_name='كود تبعية الافراد')
    person_prnt_army_name = models.CharField(max_length=100,null=True,blank=True,db_column='PERSON_PRNT_ARMY_NAME',verbose_name='كود تبعية الافراد')
    person_army_code = models.CharField(max_length=4,null=True,blank=True,db_column='ARMY_CODE',verbose_name='كود سلاح الافراد')
    person_army_name = models.CharField(max_length=100,null=True,blank=True,db_column='ARMY_NAME',verbose_name='سلاح الافراد')
    person_serv_army_code = models.CharField(max_length=4,null=True,blank=True,db_column='SERV_ARMY_CODE',verbose_name='كود سلاح الخدمة')
    person_serv_name = models.CharField(max_length=100,null=True,blank=True,db_column='SERV_NAME',verbose_name='سلاح الخدمة')
    total = models.IntegerField(null=True,blank=True,db_column='TOTAL',verbose_name='الاجمالي')
    st_10 = models.IntegerField(null=True,blank=True,db_column='ST_10',verbose_name='تسجيل')
    st_20 = models.IntegerField(null=True,blank=True,db_column='ST_20',verbose_name='مراجعة')
    st_30 = models.IntegerField(null=True,blank=True,db_column='ST_30',verbose_name='تصديق دخول اللجنة')
    st_40 = models.IntegerField(null=True,blank=True,db_column='ST_40',verbose_name='منتظر انعقاد اللجنة') 
    st_50 = models.IntegerField(null=True,blank=True,db_column='ST_50',verbose_name='حضور اللجنة')
    st_60 = models.IntegerField(null=True,blank=True,db_column='ST_60',verbose_name='عدم الحضور')
    st_70 = models.IntegerField(null=True,blank=True,db_column='ST_70',verbose_name='مثول امام اللجنة')
    st_99 = models.IntegerField(null=True,blank=True,db_column='ST_99',verbose_name='لم يصدق علي دخول اللجنة')

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        ordering= ['person_army_code','person_prnt_army_code','person_serv_army_code']
        db_table = 'V_COMM_PER_STATUS'




class LagnaAfrOpinionsReport(models.Model):
    row_id = models.BigAutoField(primary_key=True,db_column='ROW_ID')
    committe_code = models.ForeignKey(Lagna,related_name='opinions_report',on_delete=models.DO_NOTHING,db_column='COMMITTE_CODE')
    committe_name = models.CharField(max_length=150,null=True,blank=True,db_column='COMMITTE_NAME')
    spacific_code = models.ForeignKey(LagnaTypeSpacific,related_name='opinions_report',on_delete=models.DO_NOTHING,db_column='COMM_DA_TYPE_ID')
    type_name = models.CharField(max_length=150,null=True,blank=True,db_column='TYPE_NAME')
    army_code = models.ForeignKey(ArmyCode,on_delete=models.DO_NOTHING,related_name='opinions_report',db_column='ARMY_CODE')
    army_name = models.CharField(max_length=150,null=True,blank=True,db_column='ARMY_NAME')
    prnt_army_code	= models.ForeignKey(ArmyCode,on_delete=models.DO_NOTHING,related_name='prnt_opinions_report',db_column='PRNT_ARMY_CODE')
    prnt_army_name = models.CharField(max_length=150,null=True,blank=True,db_column='PRNT_ARMY_NAME')
    opinion_code = models.ForeignKey(OpinionType,on_delete=models.DO_NOTHING,related_name='opinions_report',db_column='OPINION_CODE')
    opinion_name = models.CharField(max_length=150,null=True,blank=True)
    vote_code = models.ForeignKey(LagnaVoteOpinoin,on_delete=models.DO_NOTHING,related_name='opinions_report',db_column='OT_OPINION_TYPE_ID')
    vote_name =models.CharField(max_length=150,null=True,blank=True,db_column='OT_OPINION_NAME') 
    total = models.IntegerField(null=True,blank=True,db_column='TOTAL')

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        ordering = ['committe_code','spacific_code','spacific_code__committe_type','army_code','prnt_army_code','opinion_code']
        db_table = 'V_COMM_PER_OPINIONS'