from django.db import models
from django.conf import settings
db_engine = settings.DATABASES['default']['ENGINE']

# Create your models here.

class ArmyCode(models.Model):
    army_code = models.CharField(primary_key=True,null=False,max_length=4)
    army_name = models.CharField(max_length=100,null=False)
    army_chk = models.BooleanField(null=True,blank=True)

    def __str__(self):
        return self.army_name
    


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        ordering = ['army_code']
        if 'oracle' in db_engine:
            db_table = '"HAYAA"."COD_ARMY_CODE"'
        else:
            db_table = "COD_ARMY_CODE"






class Rank(models.Model):
    rank_code = models.BigAutoField(primary_key=True,null=False,db_column='RANK_CODE')
    rank_name = models.CharField(null=False,blank=False,max_length=30,db_column='RANK_NAME')
    rank_sort = models.IntegerField(null=True,blank=True,db_column='RANK_SORT')

    def __str__(self):
        return self.rank_name


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        # db_table = '"HAYAA"."RANK_CODE"'
        ordering = ['rank_name']
        if 'oracle' in db_engine:
            db_table = '"HAYAA"."RANK_CODE"'
        else:
            db_table = "RANK_CODE"

class ArmyParentChild(models.Model):
    id = models.IntegerField(primary_key=True)
    child_code = models.CharField(null=False,max_length=4)
    child_name = models.CharField(null=False,max_length=255)
    parent_code	= models.CharField(null=False,max_length=4)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'CH_PAR_ARMY_CODE'


class Jobs(models.Model):
    job_id = models.BigAutoField(primary_key=True,db_column='JOB_ID')
    job_name = models.TextField(null=False,max_length=250,db_column='JOB_NAME')
    job_order = models.IntegerField(null=True,blank=True,db_column='JOB_ORDER')
    active_flag = models.BooleanField(default=True,null=True,blank=True,db_column='ACTIVE_FLAG')
    delete_flag = models.BooleanField(default=False,null=True,blank=True,db_column='DELETE_FLAG')

    def __str__(self):
        return self.job_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'JOBS'
        ordering = ['job_order']

        
class FamilyDegreeCode(models.Model):
    degree_code = models.IntegerField(primary_key=True,db_column='DEGREE_CODE')
    degree_name = models.CharField(max_length=100,null=False,blank=False,db_column='DEGREE_NAME')
    degree_order = models.IntegerField(null=True,blank=True,db_column='DEGREE_ORDER')

    class Meta:
        db_table = 'FAMILY_DEGREE_CODE'
        ordering = ['degree_order']