from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
import os
from datetime import datetime
from django.utils import timezone

from django.conf import settings
db_engine = settings.DATABASES['default']['ENGINE']
# Create your models here.

class AfrDegree(models.Model):
    degree_code	= models.CharField(primary_key=True,null=False,max_length=4,db_column='DEGREE_CODE',db_index=True)
    degree_name	= models.CharField(max_length=255,null=False)
    degree_order = models.IntegerField(null=True,blank=True)
    ag_maash = models.IntegerField(null=True,blank=True)
    degree_code_job = models.IntegerField(null=True,blank=True)
    degree_first_salary	= models.IntegerField(null=True,blank=True)
    degree_last_salary = models.IntegerField(null=True,blank=True)
    deg_period_before_94 = models.IntegerField(null=True,blank=True)
    deg_period_after_94 = models.IntegerField(null=True,blank=True)
    max_year = models.IntegerField(null=True,blank=True)
    education_test_period = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.degree_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        # db_table = '"HAYAA"."COD_DEGREE_CODE_PERSON"'
        ordering = ['degree_code']
        if 'oracle' in db_engine:
            db_table = '"HAYAA"."COD_DEGREE_CODE_PERSON"'
        else:
            db_table = "COD_DEGREE_CODE_PERSON"


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(person_status_code__in=[1,2])




class AfrPerson(models.Model):
    mil_ser = models.CharField(primary_key=True,null=False,max_length=20)
    mil_no = models.CharField(null=False,max_length=30,unique=True)
    # degree_code = models.IntegerField(null=False)
    degree_code = models.ForeignKey(AfrDegree,on_delete=models.DO_NOTHING,related_name='afr_person',db_column='DEGREE_CODE',null=True,blank=True)
    degree_name = models.CharField(max_length=50,null=False,)
    person_name = models.CharField(max_length=150,null=False)
    person_status_code = models.IntegerField(null=True,blank=True)
    army_code = models.IntegerField(null=True,blank=True)
    army_name = models.CharField(max_length=100,null=True,blank=True)
    serv_army_code = models.IntegerField(null=True,blank=True)
    serv_name = models.CharField(max_length=100,null=True,blank=True)
    unit_code = models.CharField(null=True,blank=True,max_length=10)
    unit_name = models.CharField(max_length=150,null=True,blank=True)
    come_in_date = models.DateTimeField(null=True,blank=True)
    to_unit_date = models.DateTimeField(null=True,blank=True)
    fea_code = models.IntegerField(null=False)
    fea_name = models.CharField(max_length=50,null=False)
    work_traning_code = models.IntegerField(null=True,blank=True)
    army_job_name = models.CharField(max_length=150,null=True,blank=True)
    birth_date = models.DateTimeField(null=True,blank=True)
    tot_years = models.IntegerField(null=True,blank=True)
    rateb_date = models.DateTimeField(null=True,blank=True)
    tot_rateb = models.IntegerField(null=True,blank=True)
    tot_ser_y = models.IntegerField(null=True,blank=True)
    tot_ser_m = models.IntegerField(null=True,blank=True)
    curr_degree_date = models.DateTimeField(null=True,blank=True)
    person_adress = models.CharField(max_length=150,null=True,blank=True)
    add_markaz_code = models.IntegerField(null=True,blank=True)
    markaz_name = models.CharField(max_length=40,null=True,blank=True)
    add_mohafza_code = models.IntegerField(null=True,blank=True)
    mohafza_name = models.CharField(max_length=50,null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    length = models.IntegerField(null=True,blank=True)
    consis = models.IntegerField(null=True,blank=True)
    consis_name = models.CharField(max_length=8,null=True,blank=True)
    person_mil_order = models.IntegerField(null=True,blank=True)
    marital_state_code = models.IntegerField(null=True,blank=True)
    marital_state_name = models.CharField(null=True,blank=True,max_length=150)
    upgrade_date = models.DateTimeField(null=True,blank=True)
    unit_interval_y = models.IntegerField(null=True,blank=True)
    unit_interval_m = models.IntegerField(null=True,blank=True)
    unit_interval_d = models.IntegerField(null=True,blank=True)
    prnt_army_code = models.IntegerField(null=True,blank=True)
    prnt_army_name = models.CharField(max_length=100)
    over_weight = models.IntegerField(null=True,blank=True)
    tarakymogmed_flag = models.BooleanField(null=True,blank=True)
    tarakymogmed_reason = models.CharField(null=True,blank=True,max_length=200)
    person_sex_code = models.IntegerField(null=True,blank=True)
    person_sex_name = models.CharField(null=True,blank=True,max_length=255)
    

    objects = ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.person_name

    

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_PER_DATA'
        ordering = ['army_code','person_sex_code','degree_code__degree_order','mil_no']
        # ordering = ['mil_ser__prnt_army_code','-mil_ser__person_sex_code','mil_ser__degree_code__degree_order','mil_ser__mil_no']
        permissions  = [
            ('can_see_all_people','can see all people')
        ]


class FamilyManager(models.Manager):
    
    def get_father(self):
        return self.get_queryset().filter(relation_degree_code =  1)

    def get_mother(self):
        return self.get_queryset().filter(relation_degree_code_id = 2)
    
    def get_curr_wifies(self):
        return self.get_queryset().filter(Q(relation_degree_code__in =[], onlife_or_not = False))
    
    def get_prev_wifies(self):
        return self.get_queryset().filter(Q(relation_degree_code__in =[], onlife_or_not = False)|Q(relation_degree_code__in =[]))

    def get_pro(self):
        return self.get_queryset().filter(relation_degree_code__in = [])
    
    def get_relatives(self):
        return self.get_queryset().filter(relation_degree_code__in = [])

    def get_children(self):
        return self.get_queryset().filter(relation_degree_code__in = [])
    def get_live_children(self):
        return self.get_queryset().filter(relation_degree_code__in = [],onlife_or_not=True)


class Family(models.Model):

    fam_id = models.BigAutoField(primary_key=True,null=False)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.CASCADE,related_name='family',db_column='MIL_SER')
    per_name = models.CharField(null=True,blank=True,max_length=100)
    relation_degree_code = models.IntegerField(null=True,blank=True,db_column='RELATION_DEGREE_CODE')
    relation_degree_name = models.CharField(null=True,blank=True,max_length=50)
    address = models.CharField(null=True,blank=True,max_length=150)    
    telphone_no = models.CharField(null=True,blank=True,max_length=100)
    marry_no = models.CharField(null=True,blank=True,max_length=20)
    marry_date = models.DateTimeField(null=True,blank=True)
    notes = models.CharField(null=True,blank=True,max_length=255)
    kawmy_number = models.CharField(null=True,blank=True,max_length=14)
    resp_birth_date = models.DateTimeField(null=True,blank=True)
    birth_year = models.IntegerField(null=True,blank=True,db_column='B_Y')
    birth_month = models.IntegerField(null=True,blank=True,db_column='B_M')
    birth_day = models.IntegerField(null=True,blank=True,db_column='B_D')
    wife_order = models.IntegerField(null=True,blank=True)
    diana_code = models.IntegerField(null=True,blank=True)
    diana_name = models.CharField(null=True,blank=True,max_length=50)
    onlife_or_not = models.BooleanField(null=True,blank=True)
    resp_job_code = models.IntegerField(null=True,blank=True)
    is_married = models.BooleanField(null=True,blank=True)
    dead_date = models.DateTimeField(null=True,blank=True)
    nationality = models.IntegerField(null=True,blank=True)
    relative_wife_name = models.CharField(null=True,blank=True,max_length=100)
    relative_wife_moahl = models.CharField(null=True,blank=True,max_length=140)
    get_data_date = models.DateTimeField(null=True,blank=True)

    objects = FamilyManager()


    class Meta:
        db_table = 'AFR_SEG_FAMILY'
        ordering = ['kawmy_number','relation_degree_code']
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)


class FamilyStatistic(models.Model):
    fs_id = models.IntegerField(primary_key=True,db_column='FS_ID')
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.CASCADE,related_name='family_statistic',db_column='MIL_SER')
    father_job = models.CharField(max_length=255,null=True,blank=True,db_column='FATHER_JOB')
    mother_job = models.CharField(max_length=255,null=True,blank=True,db_column='MOTHER_JOB')
    whife_job = models.CharField(max_length=255,null=True,blank=True,db_column='WHIFE_JOB')
    relativ = models.IntegerField(null=True,blank=True,db_column='RELATIV')
    curr_marrige = models.IntegerField(null=True,blank=True,db_column='CURR_MARRIGE')
    prev_marrige = models.IntegerField(null=True,blank=True,db_column='PREV_MARRIGE')
    son = models.IntegerField(null=True,blank=True,db_column='SON')
    doughter = models.IntegerField(null=True,blank=True,db_column='DOUGHTER')
    sister = models.IntegerField(null=True,blank=True,db_column='SISTER')
    brother = models.IntegerField(null=True,blank=True,db_column='BROTHER')


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'MV_FAMILY_STATISTIC'
        ordering = ['fs_id','mil_ser']



class AfrPunishment(models.Model):
    row_id = models.BigAutoField(primary_key=True,null=False,db_column='PUN_ID')
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.SET_NULL,null=True,related_name='person_punishment',db_column='MIL_SER')
    per_punsh_ser = models.IntegerField(null=False)
    crime_code =  models.IntegerField(null=False)

    crime_period = models.IntegerField(null=True,blank=True)
    crime_name = models.CharField(null=True,blank=True,max_length=360)
    crime_law = models.CharField(null=True,blank=True,max_length=250)
    low_part_no = models.CharField(null=True,blank=True,max_length=250)
    mokhala_or_not = models.BooleanField(null=True,blank=True)
    mokhala = models.CharField(null=True,blank=True,max_length=11)
    crime_date = models.DateTimeField(null=False)
    punsh_cort_code = models.IntegerField(null=True,blank=True)
    punsh_cort=models.CharField(null=True,blank=True,max_length=40)
    punishment_code = models.CharField(max_length=10,null=True,blank=True)
    punishment_name = models.CharField(null=True,blank=True,max_length=80)
    punish_period = models.IntegerField(null=True,blank=True)
    punish_start_date = models.DateTimeField(null=True,blank=True)
    punish_end_date = models.DateTimeField(null=True,blank=True)
    band_no = models.CharField(null=True,blank=True,max_length=150)
    band_date = models.DateTimeField(null=True,blank=True)
    punish_per_code = models.IntegerField(null=True,blank=True)
    punish_per_name = models.CharField(null=True,blank=True,max_length=70)
    cort_no = models.CharField(max_length=150,null=True,blank=True)
    cort_date = models.DateTimeField(null=True,blank=True)
    notes = models.CharField(null=True,blank=True,max_length=1000) # must be changed in the future
    crime_major = models.IntegerField(null=True,blank=True)
    cort_place = models.CharField(null=True,blank=True,max_length=80)
    rad_eeatabar_date = models.DateTimeField(null=True,blank=True)
    neaba_desc_no = models.CharField(null=True,blank=True,max_length=100)
    neaba_desc_date = models.DateTimeField(null=True,blank=True)
    punish_type = models.IntegerField(null=True,blank=True)
    get_data_date = models.DateTimeField(null=True,blank=True)
    period_day= models.IntegerField(null=True,blank=True,db_column='DA')
    period_month = models.IntegerField(null=True,blank=True,db_column='MON')
    period_year = models.IntegerField(null=True,blank=True,db_column='YE')


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        ordering= ['mil_ser','per_punsh_ser','crime_code','crime_date']
        db_table = 'AFR_SEG_PUNISHMENT'
        constraints = [
            models.UniqueConstraint(
                fields=['mil_ser','per_punsh_ser','crime_code','crime_period','crime_date','punish_start_date'],
                name="mil_ser_per_punsh_ser_crime_code_crime_peroid_crime_date_punish_start_date",
            )
        ]


class AfrTagdedHistroy(models.Model):
    row_id = models.BigAutoField(primary_key=True,null=False,db_column='ROW_ID')
    upgra = models.IntegerField(null=True,blank=True)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.CASCADE,related_name='tagded_history',db_column='MIL_SER')
    nashra_code = models.IntegerField()
    nashra_name = models.CharField(max_length=60)
    nashra_status_code = models.IntegerField()
    nashra_status_name = models.CharField(max_length=60,null=True,blank=True)
    refuse_reson_code = models.IntegerField(null=True,blank=True)
    refuse_reson_name = models.CharField(max_length=80,null=True,blank=True)
    degree_code = models.IntegerField(null=True,blank=True)
    degree_name = models.CharField(max_length=50)
    from_date = models.DateTimeField(null=True,blank=True)
    to_date = models.DateTimeField(null=True,blank=True)
    lost_period_in_daies = models.IntegerField(null=True,blank=True)
    interview_result = models.IntegerField(null=True,blank=True)
    length = models.IntegerField(null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    manager_opinion = models.IntegerField(null=True,blank=True)
    consistency_flag = models.IntegerField(null=True,blank=True)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        ordering = ['mil_ser','nashra_code','degree_code','to_date']
        db_table = 'AFR_TAGDED_TARAKY_DATA'



class  PersonEffecincy(models.Model):
    eff_num = models.BigAutoField(primary_key=True,null=False)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.SET_NULL,null=True,related_name='effecincy',db_column='MIL_SER')
    degree_code = models.IntegerField(null=False)
    unit_code = models.CharField(null=True,blank=True,max_length=50)
    unit_name = models.CharField(null=True,blank=True,max_length=1000)
    from_date = models.DateTimeField(null=True,blank=True)
    to_date = models.DateTimeField(null=True,blank=True)
    direct_per_grade = models.IntegerField(null=True,blank=True)
    grade_name = models.CharField(max_length=20,null=True,blank=True)
    sign_per_grade = models.IntegerField(null=True,blank=True)
    sign_grade_name = models.CharField(max_length=20,null=True,blank=True)
    direct_per_notes = models.CharField(max_length=200,null=True,blank=True)
    direct_per_reasons = models.CharField(max_length=200,null=True,blank=True)
    direct_per_name = models.CharField(max_length=200,null=True,blank=True)
    direct_per_date = models.DateTimeField(null=True,blank=True)
    sign_per_decision = models.CharField(max_length=200,null=True,blank=True)
    sign_per_name = models.CharField(max_length=200,null=True,blank=True)
    sign_per_notes = models.CharField(max_length=200,null=True,blank=True)
    sign_per_job = models.CharField(max_length=200,null=True,blank=True)
    sign_per_date = models.DateTimeField(null=True,blank=True)
    modification_time = models.DateTimeField(auto_now_add=True)
    creation_time = models.DateTimeField(auto_now=True)
    
    effecincy_report_type = models.IntegerField(null=True,blank=True)
    get_data_date = models.DateTimeField(null=True,blank=True)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_SEG_EFFECINCY'
        ordering = ['eff_num','mil_ser','unit_code','degree_code','to_date','direct_per_grade','grade_name']

class PersonEffecincyL3Y(models.Model):
    th_id = models.IntegerField(primary_key=True,null=False,db_column='TH_ID')
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.CASCADE,related_name='person_effecincy_l3y',db_column='MIL_SER')
    degree_code = models.IntegerField(null=True,blank=True)
    grade_name = models.CharField(max_length=20,null=True,blank=True)
    unit_code = models.CharField(max_length=50,null=True,blank=True)
    unit_name = models.CharField(max_length=1000,null=True,blank=True)
    sign_grade_name = models.CharField(max_length=20,null=True,blank=True)
    direct_per_notes = models.CharField(max_length=200,null=True,blank=True)
    direct_per_reasons = models.CharField(max_length=200,null=True,blank=True)
    direct_per_name = models.CharField(max_length=200,null=True,blank=True)
    direct_per_date = models.DateTimeField(null=True,blank=True)
    sign_per_decision = models.CharField(max_length=200,null=True,blank=True)
    sign_per_name = models.CharField(max_length=200,null=True,blank=True)
    sign_per_notes = models.CharField(max_length=200,null=True,blank=True)
    from_date = models.DateTimeField(null=True,blank=True)
    to_date = models.DateTimeField(null=True,blank=True)
    creation_user = models.CharField(max_length=200,null=True,blank=True)
    creation_time = models.DateTimeField(null=True,blank=True)
    effecincy_report_type = models.IntegerField(null=True,blank=True)
    ord = models.IntegerField(null=True,blank=True)
    direct_per_grade = models.IntegerField(null=True,blank=True)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'MV_LAST_THREE_EF_REPORT'
        ordering = ['th_id','mil_ser','degree_code','unit_code']


class PersonEffecincyAvg(models.Model):
    av_id = models.IntegerField(primary_key=True)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.CASCADE,related_name='person_effecincy_avg',db_column='MIL_SER')
    grade = models.CharField(max_length=155,null=True,blank=True)
    tot_co = models.IntegerField(null=True,blank=True)
    roun = models.IntegerField(null=True,blank=True)
    su = models.IntegerField(null=True,blank=True)


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'MV_AV_LAST_THREE_EF_REPORT'
        ordering = ['av_id','mil_ser','roun','grade']




class PunishmentStatistics(models.Model):
    stat_id = models.IntegerField(primary_key=True,null=False)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.SET_NULL,null=True,related_name='statistics',db_column='MIL_SER')
    oth  = models.IntegerField(null=True,blank=True)
    stay= models.IntegerField(null=True,blank=True)
    not_stay= models.IntegerField(null=True,blank=True)
    tot_pa= models.IntegerField(null=True,blank=True)
    court= models.IntegerField(null=True,blank=True)


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'MV_PER_PUNISHMENT_STATIC'


class MedicalLagnaResultLookUp(models.Model):
    lagna_result_id = models.BigAutoField(primary_key=True,db_column='LAGNA_RESULT_ID')
    result = models.CharField(null=False,max_length=500,db_column='LAGNA_RESULT')
    def __str__(self):
        return self.result
    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'LK_MEDICAL_LAGNA_RESULT'

class MedicalHistory(models.Model):
    mag_lag_id =  models.BigAutoField(primary_key=True,null=False)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.SET_NULL,null=True,related_name='medical_history',db_column='MIL_SER')
    paper_no = models.CharField(max_length=30,null=False)
    paper_date = models.DateTimeField(null=True,blank=True)
    unit_code = models.CharField(max_length=100,null=False)
    paper_date_segelat = models.DateTimeField(null=True,blank=True)
    is_done = models.IntegerField(null=False)
    get_data_date = models.DateTimeField(null=True,blank=True)
    lagna_result = models.ForeignKey(MedicalLagnaResultLookUp,on_delete=models.DO_NOTHING,null=True,blank=True,db_column='LAGNA_RESULT')
    lagna_date = models.DateTimeField(null=True,blank=True)
    tashkhes = models.CharField(max_length=150,null=True,blank=True)
    unit_name = models.CharField(max_length=150,null=True,blank=True)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table='AFR_SEG_MAGLES_LAGNA_ADNA'



class AfrEducation(models.Model):
    edu_id = models.BigAutoField(primary_key=True,null=False)
    dawra_no  = models.IntegerField(null=True,blank=True)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.SET_NULL,null=True,related_name='education',db_column='MIL_SER')

    per_mil_edu_ser = models.IntegerField(null=True,blank=True)
    dawra_code = models.IntegerField(null=True,blank=True)
    dawra_name = models.CharField(max_length=100,null=True,blank=True)
    dawra_name_detail = models.CharField(max_length=70,null=True,blank=True)
    grade_code = models.IntegerField(null=True,blank=True)
    grade_name = models.CharField(max_length=20,null=True,blank=True)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    notes = models.TextField(max_length=255,null=True,blank=True)
    get_data_date = models.DateTimeField(null=True,blank=True)
    unit_name = models.CharField(max_length=150,null=True,blank=True)
    dawra_place = models.CharField(max_length=150,null=True,blank=True)
    refuse_reason = models.TextField(max_length=50,null=True,blank=True)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_SEG_EDUCATION'
        ordering = ['mil_ser','-start_date']



class AfrUnits(models.Model):
    per_unit_id = models.BigAutoField(primary_key=True,null=False)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.SET_NULL,related_name='units',null=True,db_column='MIL_SER')
    per_unit_ser = models.IntegerField(null=False)

    unit_code = models.CharField(max_length=25,null=False)
    unit_name = models.CharField(max_length=150,null=False,blank=False)

    to_unit_date = models.DateTimeField(null=True,blank=True)
    from_unit_date = models.DateTimeField(null=True,blank=True)

    band_date = models.DateTimeField(null=True,blank=True)
    education_type_code = models.IntegerField(null=True,blank=True)
    work_traning_code = models.IntegerField(null=True,blank=True)
    notes = models.TextField(max_length=255,null=True,blank=True)
    chk = models.CharField(max_length=150,null=True,blank=True)
    serv_type_code = models.IntegerField(null=True,blank=True)
    band_no = models.CharField(max_length=20,null=True,blank=True)

    get_data_date = models.DateTimeField(null=True,blank=True)


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_SEG_UNIT'
        
        constraints = [
            models.UniqueConstraint(
                fields=['mil_ser','per_unit_ser','unit_code','unit_name','to_unit_date','from_unit_date','band_date','education_type_code','work_traning_code','notes','band_no'],
                name="constraints_on_all_fields",
            )
        ]





class AfrTravel(models.Model):
    tr_id	= models.BigAutoField(primary_key=True)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.SET_NULL,null=True,related_name='travel',db_column='MIL_SER')
    # d_type = models.CharField(max_length=255,null=True,blank=True)
    safar_eara_reason_code = models.IntegerField(null=True,blank=True)
    safar_eara_reason_name 	= models.CharField(max_length=255,null=True,blank=True)
    country_code = models.IntegerField(null=True,blank=True)
    country_name	= models.CharField(max_length=255,null=True,blank=True)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date	= models.DateTimeField(null=True,blank=True)
    peroid_year = models.IntegerField(null=True,blank=True,db_column='YE')
    peroid_month = models.IntegerField(null=True,blank=True,db_column='MON')
    peroid_day = models.IntegerField(null=True,blank=True,db_column='DA')
    # locations	= models.CharField(max_length=255,null=True,blank=True)
    # tasdyk_code	= models.IntegerField(null=True,blank=True)
    # tasdyk_name	= models.CharField(max_length=255,null=True,blank=True)
    # tasdyk_no	= models.CharField(max_length=255,null=True,blank=True)
    # tasdyk_date	= models.DateTimeField(null=True,blank=True)
    # status_code	= models.IntegerField(null=True,blank=True)
    # status_name	= models.CharField(max_length=255,null=True,blank=True)
    get_data_date	= models.DateTimeField(null=True,blank=True)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_PER_TRAVEL'
        ordering = ['-end_date']

class AfrVacation(models.Model):
    id = models.IntegerField(primary_key=True,db_column='VACATION_ID')
    mil_ser	= models.ForeignKey(AfrPerson,related_name='vacation',on_delete=models.DO_NOTHING,null=False,db_column='MIL_SER')
    vacation_ser = models.IntegerField(null=True,blank=True,db_column='VACATION_SER')
    vacation_code = models.CharField(null=True,blank=True,max_length=10,db_column='VACATION_CODE')
    vacation_name = models.CharField(null=True,blank=True,max_length=30,db_column='VACATION_NAME')
    start_date = models.DateTimeField(null=True,blank=True,db_column='VACATION_START_DATE')
    end_date = models.DateTimeField(null=True,blank=True,db_column='VACATION_END_DATE')
    notes = models.TextField(max_length=50,null=True,blank=True,db_column='NOTES')
    come_back = models.BooleanField(null=True,blank=True,db_column='COME_BACK')
    creation_time = models.DateTimeField(null=True,blank=True,db_column='CREATION_TIME')

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_SEG_VACATION'
        ordering = ['start_date','end_date','come_back']
        



def attach_upload_to(obj,filename):
    name,ext = os.path.splitext(filename)
    new_name = f'{obj.mil_ser.mil_no}_{obj.mil_ser.degree_code_id}{ext}'
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_path= os.path.join(str(obj.mil_ser.army_code),str(obj.mil_ser.mil_no),'psychological_report',timestamp,new_name)
    return new_path

class AfrPsychologicalReport(models.Model):
    psych_id = models.BigAutoField(primary_key=True,null=False)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.DO_NOTHING,null=False,related_name='psycholgical_report',db_column='MIL_SER')

    report_date	= models.DateTimeField(null=False)
    psych_notes	 = models.CharField(null=False,blank=False,max_length=2000)
    psych_attach  = models.ImageField(null=True,blank=True,upload_to=attach_upload_to)

    create_user	 = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='mil_ser_psychological',db_column='CREATE_USER')
    create_date	 = models.DateTimeField(auto_now_add=True)

    active_flag	= models.BooleanField(default = True)
    delete_flag	= models.BooleanField(default=False)
    delete_user	= models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='mil_ser_psychological_delete',db_column='DELETE_USER')
    delete_date	= models.DateTimeField(null=True,blank=True)


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'PSYCHOLOGICAL_REPORT'

class SecurityActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_flag=True,delete_flag=False)


def sec_attach_upload_to(obj,filename):
    name,ext = os.path.splitext(filename)
    new_name = f'{obj.mil_ser.mil_no}_{obj.mil_ser.degree_code}{ext}'
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_path= os.path.join(str(obj.mil_ser.army_name),str(obj.mil_ser.mil_no),'security',timestamp,new_name)
    return new_path


class AfrSecuritySituation(models.Model):
    secu_id = models.BigAutoField(primary_key=True,null=False)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.DO_NOTHING,null=False,related_name='security',db_column='MIL_SER')
    notes = models.CharField(null=False,max_length=1000,db_column='SECU_NOTES')
    attached = models.ImageField(null=True,blank=True,upload_to=sec_attach_upload_to,db_column='SECU_ATTACHED')

    active_flag = models.BooleanField(default=True)
    create_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,related_name='create_afr_security',db_column='CREATE_USER')
    create_date = models.DateTimeField(auto_now_add=True)

    delete_flag = models.BooleanField(default=False)
    delete_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='delete_afr_security',db_column='DELETE_USER')
    delete_date = models.DateTimeField(null=True,blank=True)
    objects = SecurityActiveManager()
    all_objects = models.Manager()

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_SECURITY_DETAIL'

