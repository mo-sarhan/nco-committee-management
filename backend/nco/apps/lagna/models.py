from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from apps.person.models import AfrPerson
from datetime import datetime
from apps.tanzem.models import (Rank,ArmyCode,Jobs)
import os

# Create your models here.


class LagnaStatusType(models.Model):
    status_code = models.BigAutoField(primary_key=True,db_column='STATUS_CODE')
    status_name = models.CharField(unique=True,max_length=255,null=False,blank=False)
    active_flag = models.BooleanField(default=True)
    delete_flag= models.BooleanField(default=False)

    class Meta:
        managed = getattr(settings,'MANAGED_MIGRATIONS',False)
        db_table = 'LAGNA_STATUS_TYPE'
        ordering = ['status_code'] 

class LagnaType(models.Model):
    type_id = models.IntegerField(primary_key=True,null=False)
    type_name = models.CharField(max_length=500,null=True,blank=True)
    active_flag = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    delete_flag = models.BooleanField(default=False)
    delete_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.type_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table= 'COMMITTE_TYPE'
        ordering = ['type_id']
        constraints = [
            models.UniqueConstraint(
                fields=['type_name'],
                name='type_id_type_name'
            )
        ]

class LagnaCategory(models.Model):
    category_id = models.IntegerField(primary_key=True,null=False)
    category_name = models.CharField(max_length=500,null=True,unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    active_flag = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

    def delete(self,*args,**kwargs):
        self.delete_flag = True
        self.active_flag = False
        self.save()

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'COMMITEE_CATEGORY'
        constraints = [
            models.UniqueConstraint(
                fields=['category_id','category_name'],
                name='category_id_names'
            )
        ]
        
        
class VoteType(models.Model):
    vote_type_code = models.IntegerField(primary_key=True,null=False)
    vote_type_name = models.CharField(null=False,unique=True,max_length=250)
    active_flag	 = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.vote_type_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'VOTE_TYPE'


class LagnaMemberType(models.Model):
    member_type_code = models.IntegerField(primary_key=True,null=False,db_column='MEMBER_TYPE_CODE')
    vote_type = models.ForeignKey(VoteType,on_delete=models.DO_NOTHING,null=False,db_column='VOTE_TYPE')
    member_type_name = models.CharField(max_length=100,null=False,blank=False)
    socket_group = models.CharField(max_length=100,null=True,blank=False,db_column='SOCKET_GROUP')
    open_final_decision = models.BooleanField(default=0,null=True,blank=True,db_column='OPEN_FINAL_DECISION')
    active_flag = models.BooleanField(default=True,db_column='ACTIVE_FLAG')
    delete_flag = models.BooleanField(default=False,db_column='DELETE_FLAG')

    def __str__(self):
        return self.member_type_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'COMMITTE_MEMBER_TYPE'
        ordering = ['vote_type']



class LagnaVoteOpinoin(models.Model):
    opinion_code = models.BigAutoField(primary_key=True,null=False,unique=True)
    opinion_name = models.CharField(max_length=50,null=True,blank=True)
    committe_type_code = models.ForeignKey(LagnaType,on_delete=models.SET_NULL,related_name='vote_opinoin',null=True,db_column='COMMITTE_TYPE_CODE')
    active_flag = models.BooleanField(default = True)
    classifie_code = models.IntegerField(null=True,blank=True)
    delete_flag = models.BooleanField(default=False)


    def __str__(self):
        return self.opinion_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'VOTE_OPINION'
        ordering = ['opinion_code']

        constraints = [
            models.UniqueConstraint(
                fields=['opinion_code','opinion_name','committe_type_code'],
                name='opinion_code_opinion_name_committe_type_code'
            )
        ]


class LagnaAfrStatus(models.Model):
    afr_comm_status_code = models.BigAutoField(primary_key=True,null=False)
    afr_comm_status_name = models.CharField(max_length=500,null=True,blank=True)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.afr_comm_status_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table='AFR_COMM_STATUS'


def validate_lagna_date(value):
    """ Ensure the date is in the future"""
    if value.date() < timezone.localdate():
        raise ValidationError(f'the date can not be in the past {value}')


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_flag=True,delete_flag=False)

class Lagna(models.Model):

    committe_code = models.BigAutoField(primary_key=True,null=False)
    committe_name = models.CharField(null=False,max_length=500)
    main_committe_code = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='main_lagna',db_column='MAIN_COMMITTE_CODE')
    # committe_type = models.ForeignKey(LagnaType,on_delete=models.DO_NOTHING,related_name='lagna_type',null=False,db_column='COMMITTE_TYPE')

    committe_create_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='lagna',db_column='COMMITE_CREATE_USER')
    committe_create_date = models.DateTimeField(auto_now_add=True)

    committe_start_date = models.DateTimeField(null=False,blank=False,validators=[validate_lagna_date])
    committe_end_date = models.DateTimeField(null=False,blank=False,validators=[validate_lagna_date])

    committe_number = models.IntegerField(null=False,blank=False)
    committe_category = models.ForeignKey(LagnaCategory,on_delete=models.DO_NOTHING,null=False,related_name='lagna',db_column='COMMITTE_CATEGORY')

    prnt_army_code = models.ForeignKey(ArmyCode,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='lagna',db_column='PRNT_ARMY_CODE')

    committe_is_done = models.BooleanField(default=False)
    active_flag = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)
    objects = ActiveManager()
    all_objects = models.Manager()

    def clean(self):
        #----------------------------------------------------------------------
        # can not link lagna with itself
        # can not link child lagna with child lagna
        #----------------------------------------------------------------------
        if self.pk and self.main_committe_code_id == self.pk:
            raise ValidationError('can not link committe by it self')
        if self.main_committe_code and self.main_committe_code.committe_category_id != 2:
            raise ValidationError(f'can not link with non main committe {self.main_committe_code.committe_category.category_name}')

        #----------------------------------------------------------------------
        # 
        #----------------------------------------------------------------------
        if self.committe_category_id == 2 and self.prnt_army_code:
            raise ValidationError(f'لا يمكن وضع تبعية للجنة الرئيسية')
        # print('#'*30,self.committe_category_id)
        if (self.committe_category_id == 1) and (not self.prnt_army_code):
            raise ValidationError(f'لا يمكن انشاء لجنة فرعيه بدون تبعية')
        if (self.committe_category_id == 1 ) and (not self.main_committe_code):
            raise ValidationError(f'لا يمكن انشاء لجنة فرعية بدون الربط بلجنة رئيسية')

        #---------------------------------------------------------------
        #
        #---------------------------------------------------------------
        if self.committe_end_date and self.committe_start_date:
            if self.committe_end_date.date() < self.committe_start_date.date():
                raise ValidationError(f'تاريخ انتهاء اللجنة لا يمكن ان يكون قبل تاريخ بدء اللجنة')

            
            

    def delete(self, *args, **kwargs):
        self.active_flag = False
        self.delete_flag = True
        self.save(update_fields = ['active_flag','delete_flag'])

    def save(self,*args,**kwargs):
        self.full_clean()
        return super().save(*args,**kwargs)

    def hard_delete(self, using = ..., keep_parents = ...):
        return super().delete(using, keep_parents)

    def __str__(self):
        return f'{self.committe_name}'

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'COMMITTE_DATA'
        ordering = ['-committe_code']
        constraints = [

            # for main lagna
            models.UniqueConstraint(
                fields=['committe_name','committe_start_date','committe_end_date','committe_category','active_flag'],
                name='lagna_constraints'
            ),

            # for child lagna
            models.UniqueConstraint(
                fields=['committe_name','committe_start_date','committe_end_date','committe_category','active_flag','prnt_army_code'],
                name='lagna_constraints_child',
                condition=Q(prnt_army_code__isnull = False)
            ),

        ]
        permissions = [
            ('can_see_main_lagna','can set main lagna'),
        ]





class LagnaTypeSpacific(models.Model):

    lagna_type_id = models.BigAutoField(primary_key=True,null=False,db_column='COMM_DA_TYPE_ID')

    committe_type =models.ForeignKey(LagnaType,on_delete=models.DO_NOTHING,related_name='lagna_type_spacific',db_column='COMMITTE_TYPE')
    committe_code = models.ForeignKey(Lagna,on_delete=models.DO_NOTHING,null=False,related_name='lagna_type_spacific',db_column='COMMITTE_CODE')

    start_date = models.DateTimeField(null=False,validators=[validate_lagna_date],db_column='COMM_DA_TY_START_DATE')
    end_date	 = models.DateTimeField(null=False,validators=[validate_lagna_date],db_column='COMM_DA_TY_END_DATE')

    done_flag = models.BooleanField(default=False,db_column='COMM_DA_TY_DONE_FLAG')

    create_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='lagna_type_spacific',db_column='COMM_DA_TY_CRETAE_USER')
    create_date	= models.DateTimeField(auto_now_add=True,db_column='COMM_DA_TY_CREATE_DATE')

    active_flag = models.BooleanField(default=True,db_column='COMM_DA_TY_ACTIVE_FLAG')
    delete_flag = models.BooleanField(default=False,db_column='COMM_DA_TY_DELETE_FLAG')
    delete_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='lagna_type_spacific_deleted',db_column='COMM_DA_TY_DELETE_USER')
    delete_date = models.DateTimeField(null=True,blank=True,db_column='COMM_DA_TY_DELETE_DATE')

    def __str__(self):
        return self.committe_code.committe_name + ' ' + self.committe_type.type_name

    def clean(self):
        if not (self.committe_code.committe_start_date and  self.committe_code.committe_end_date):
            raise ValidationError(f'يجب وضع تارخ البدء و تاريخ الانهاء للجنة الفرعية او الرئيسة {self.committe_code.committe_name}')

        if self.start_date and self.end_date:
            if self.start_date.date() < self.committe_code.committe_start_date.date():
                raise ValidationError(f'start date {self.start_date.date()} can not be less than {self.committe_code.committe_start_date.date()}')
            if self.end_date.date() > self.committe_code.committe_end_date.date():
                raise ValidationError(f'end date {self.end_date.date()} can not be greater than {self.committe_code.committe_end_date.date()}')
            if self.end_date.date() < self.start_date.date():
                raise ValidationError(f'end {self.end_date} date can not before start date {self.start_date}')

    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)

    def delete(self,*args,**kwargs):
        self.active_flag = False
        self.delete_flag = True
        self.delete_date = timezone.now()
        self.save()


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'COMMITTE_DATA_TYPE'
        ordering = ['create_date','start_date','end_date','committe_type','committe_code']
        
        constraints = [
            models.UniqueConstraint(
                fields=['committe_code','committe_type'],
                name='lagna_type_spacific_constraints'
            ),
        ]




class LagnaMember(models.Model):
    member_id = models.BigAutoField(primary_key=True,null=False,db_column='MEMBER_ID')
    committe_code = models.ForeignKey(Lagna,on_delete=models.DO_NOTHING,null=True,db_column='COMMITTE_CODE',related_name='members')
    member_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,db_column='MEMBER_USER',related_name='lagna_member')
    member_type = models.ForeignKey(LagnaMemberType,on_delete=models.DO_NOTHING,null=False,db_column='MEMBER_TYPE',related_name='lagna_member')
    create_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,db_column='CREATE_USER',related_name='created_lagna')
    create_date = models.DateTimeField(auto_now_add=True)
    delete_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,db_column='DELETE_USER',related_name='lagna_member_deleted')
    delete_date = models.DateTimeField(null=True,blank=True,db_column='DELETE_DATE')
    active_flag = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)
    objects = ActiveManager()
    all_objects =  models.Manager()


    def delete(self,*args,**kwargs):
        self.active_flag = False
        self.delete_flag = True
        self.save()


    def __str__(self):
        return self.member_user.username

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'COMMITTE_MEMBER'
        constraints = [
            models.UniqueConstraint(
                fields=['committe_code','member_user','active_flag'],
                name='lagna_member_unique_lagna_member'
            ),
            models.UniqueConstraint(
                fields=['committe_code','member_type','active_flag'],
                condition = Q(member_type_id=1),
                name='lagna_member_unique_member_type'
            )
        ]


class LagnaPersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_flag=True,delete_flag=False)

class LagnaPersons(models.Model):

    person_id = models.BigAutoField(primary_key=True,db_column='PERSON_ID',)
    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.DO_NOTHING,null=False,related_name='lagna',db_column='MIL_SER')
    committe_type_code = models.ForeignKey(LagnaTypeSpacific,on_delete=models.CASCADE,related_name='lagna_persons',db_column='COMM_DA_TYPE_ID')
    person_order_day = models.IntegerField(null=True,blank=True)
    committe_order = models.IntegerField(null=True,blank=True)
    
    person_committe_date = models.DateTimeField(null=True,blank=True)

    committe_status_code = models.ForeignKey(LagnaAfrStatus,default=10,on_delete=models.SET_NULL,null=True,related_name='lagna_person_status',db_column='COMMITTE_STATUS_CODE')

    add_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='lagna_add_user',null=False,db_column='ADD_USER')
    add_date = models.DateTimeField(auto_now_add=True)

    review_user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='lagna_review_user',db_column='REVIEW_USER',null=True,blank=True) 
    review_date = models.DateTimeField(null=True,blank=True,db_column='REVIEW_DATA')

    conf_user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='lagna_conf_user',db_column='CONF_USER',null=True,blank=True) 
    conf_date = models.DateTimeField(null=True,blank=True)

    committe_user_date = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='lagna_person_waiting_date',db_column='COMMITTE_USER_DATE',null=True,blank=True) 

    attend_user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='lagna_attend_person',db_column='ATTEND_USER',null=True,blank=True) 
    attend_user_date =models.DateTimeField(null=True,blank=True) 

    committe_decision = models.ForeignKey(LagnaVoteOpinoin,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='lagna_decision',db_column='COMMITTE_DECISION')
    committe_decision_date = models.DateTimeField(null=True,blank=True)
    committe_decision_note = models.CharField(max_length=500,null=True,blank=True)
    auth_nomination_flag = models.BooleanField(default=False)

    active_flag = models.BooleanField(default=True)

    delete_flag = models.BooleanField(default=False)
    delete_user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='lagna_delete',db_column='DELETE_USER',null=True,blank=True)
    delete_date = models.DateTimeField(null=True,blank=True)

    objects = LagnaPersonManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.mil_ser.person_name

    def delete(self, *args,**kwagrs):
        self.delete_flag=True
        self.delete_date=datetime.now()
        self.save()

    def hard_delete(self, *args,**kwargs):
        return super().delete(args,kwargs)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_COMM_PERSON'
        ordering = ['committe_order','mil_ser__army_code','mil_ser__person_sex_code','mil_ser__degree_code__degree_order','mil_ser__mil_no']
        permissions = [
            ('can_set_review','can set review'),
            ('can_set_conf','can set conf'),
            ('can_set_waiting_date','can set waiting date'),
        ]


class CommanderJobType(models.Model):
    comm_des_id = models.BigAutoField(primary_key=True,null=False)
    comm_des = models.CharField(null=False,blank=False,max_length=100,unique=True)

    def __str__(self):
        return self.comm_des

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'LK_COMM_DESIGN'




class OpinionType(models.Model):
    type_id = models.BigAutoField(primary_key=True,null=False,db_column='OPINION_TYPE_ID')
    opinion_name = models.CharField(null=False,blank=True,max_length=255,unique=True)
    comm_des_id = models.OneToOneField(CommanderJobType,on_delete=models.DO_NOTHING,related_name='opinion_type',null=True,db_column='COMM_DES_ID')
    opinion_order = models.IntegerField(null=True,blank=True,db_column='OPINION_ORDER')
    job = models.ForeignKey(Jobs,on_delete=models.DO_NOTHING,null=True,blank=True,db_column='JOB')
    active_flag = models.BooleanField(default=True,db_column='OPINION_ACTIVE_FLAG')
    delete_flag = models.BooleanField(default=False,db_column='OPINION_DELETE_FLAG')

    def __str__(self):
        return self.opinion_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'OPINION_TYPE'
        ordering = ['opinion_order']
        permissions = [
            ('can_set_opinion','can set opinion'),
            ('can_set_unit_opinion','can set unit opinion'),
            ('can_set_army_opinion','can set army opinion'),
            ('can_set_afr_opinion','can set afr opinion'),
        ]



        

class LagnaPersonVotes(models.Model):
    voted_id = models.BigAutoField(primary_key=True,db_column='VOTE_ID') 
    person_id = models.ForeignKey(LagnaPersons,on_delete=models.DO_NOTHING,related_name='votes',null=False,db_column='PERSON_ID')
    vote_member_id = models.ForeignKey(LagnaMember,on_delete=models.DO_NOTHING,null=False,related_name='votes',db_column='VOTE_MEMBER_ID') # will be forign key for lagna member 
    vote = models.ForeignKey(LagnaVoteOpinoin,on_delete=models.DO_NOTHING,null=False,related_name='lagna_vote',db_column='VOTE')
    vote_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now=True)
    delete_flag = models.BooleanField(default=False)
    delete_date = models.DateTimeField(null=True,blank=True)
    active_flag = models.BooleanField(default=True)
    # add updated_date in the future

    def delete(self, using = ..., keep_parents = ...):
        self.active_flag = False
        self.delete_flag = True
        self.delete_date = datetime.now()
        self.save()

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_COMM_VOTE'

class BenefitType(models.Model):
    benefit_id	= models.BigAutoField(primary_key=True,null=False)
    benefit_type =models.CharField(null=False,unique=True,max_length=100)
    
    def __str__(self):
        return self.benefit_type



    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'LK_BENEFIT_TYPE'



def upload_snap_attach(obj,filename):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name,ext = os.path.splitext(filename)
    new_name = f'{obj.mil_ser.mil_no}_snap{ext}'
    new_path= os.path.join('comm_attach',str(obj.root_committe_id),'snaps',str(obj.mil_ser.mil_no),timestamp,new_name)
    return new_path


class LagnaAfrSnapData(models.Model):
    snap_id = models.BigAutoField(primary_key=True,null=False)
    # person_id = models.OneToOneField(LagnaPersons,on_delete=models.DO_NOTHING,related_name='afr_snap',db_column='PERSON_ID')

    mil_ser = models.ForeignKey(AfrPerson,on_delete=models.DO_NOTHING,null=True,related_name='snaps',db_column='MIL_SER')
    root_committe = models.ForeignKey(Lagna,on_delete=models.DO_NOTHING,null=False,related_name='snaps',db_column='COMMITTE_CODE')
    committe_type = models.ForeignKey(LagnaType,on_delete=models.DO_NOTHING,null=False,related_name='snaps',db_column='TYPE_ID')

    benefit_id = models.ForeignKey(BenefitType,on_delete=models.DO_NOTHING,null=True,blank=True,related_name ='snaps',db_column='BENEFIT_ID')

    unit_code = models.CharField(null=True,blank=True,max_length=10)
    unit_name = models.CharField(null=True,blank=True,max_length=150)
    army_code = models.ForeignKey(ArmyCode,on_delete=models.DO_NOTHING,related_name='snap_army_code',null=True,db_column='ARMY_CODE')
    prnt_army_code = models.ForeignKey(ArmyCode,on_delete=models.DO_NOTHING,related_name='snap_prnt_army_code',null=True,db_column='PRNT_ARMY_CODE')
    degree_code	 = models.CharField(null=True,blank=True,max_length=255)
    to_unit_date = models.DateTimeField(null=True,blank=True)

    # سبب العرض - why this person is being put in front of the committee.
    # One free text per snap, unlike the reasons list (AFR_COMM_PERSON_REASON)
    # which holds many rows per snap.
    add_reason = models.CharField(null=True,blank=True,max_length=2000,db_column='ADD_REASON')

    attach = models.ImageField(null=True,blank=True,upload_to=upload_snap_attach,db_column='ATTACH_FILE')

    create_user	 = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='afr_snap',null=True,db_column='CREATE_USER')
    create_date	 = models.DateTimeField(auto_now_add=True)
    active_flag	 = models.BooleanField(default=True)

    delete_flag	 = models.BooleanField(default=False)
    delete_user	 =  models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='afr_snap_deleted',null=True,blank=True,db_column='DELETE_USER')
    delete_date	 = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.mil_ser.person_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_SNAP_DATA'
        constraints = [
            models.UniqueConstraint(
                fields=['mil_ser','root_committe','committe_type'],
                name='afr_snap_constraints'
            )
        ]
        

def upload_to_reason_attach(obj,filename):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_path= os.path.join('comm_attach',str(obj.person_id.committe_type_code.committe_code),str(obj.committe_type_code),str(obj.person_id),timestamp,filename)
    return new_path

class LagnaPersonReasons(models.Model):
    reason_id	= models.BigAutoField(primary_key=True)
    snap_id = models.ForeignKey(LagnaAfrSnapData,on_delete=models.DO_NOTHING,null=True,related_name='reasons',db_column='SNAP_ID')
    descrption = models.TextField(null=False,blank=False,max_length=10000,db_column='REASON_DESCRPTION')
    attach = models.ImageField(null=True,blank=True,upload_to=upload_to_reason_attach,db_column='REASON_ATTACH')
    active_flag = models.BooleanField(default=True)
    create_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='lagna_person_reasons',null=False,db_column='CREATE_USER')
    create_date	= models.DateTimeField(auto_now_add=True)
    delete_flag	= models.BooleanField(default=False)
    delete_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='lagna_person_reasons_deleted',null=True,blank=True,db_column='DELETE_USER')
    delete_date	= models.DateTimeField(null=True,blank=True)
    reason_order = models.IntegerField(null=True,blank=True)


    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_COMM_PERSON_REASON'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['snap_id','descrption'],
        #         name='lagna_comm_reason',
        #     )
        # ]


class AfrSnapActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_flag=True,delete_flag=False)


def upload_to_snap_opinion_attach(obj,filename):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name,ext = os.path.splitext(filename)
    new_name = f'{obj.snap_id.mil_ser.mil_no}{ext}'
    new_path= os.path.join('comm_attach',str(obj.snap_id.root_committe_id),'opinions',str(obj.snap_id.mil_ser.mil_no),timestamp,new_name)
    return new_path

class AfrSnapOpinion(models.Model):
    opinion_id = models.BigAutoField(primary_key=True,db_column='OPINION_ID')
    snap_id = models.ForeignKey(LagnaAfrSnapData,on_delete=models.DO_NOTHING,null=False,related_name='opinions',db_column='SNAP_ID')
    opinion_type = models.ForeignKey(OpinionType,on_delete=models.DO_NOTHING,null=False,related_name='snap_opinions',db_column='OPINION_TYPE')
    opinion_code = models.ForeignKey(LagnaVoteOpinoin,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='snap_vote',db_column='OPINION_CODE')
    opinion_notes = models.CharField(null=True,blank=True,max_length=2000,db_column='OPINION_NOTES')
    create_date = models.DateTimeField(auto_now_add=True,db_column='OPINION_CREATE_DATE')
    create_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='snap_opinion_created',db_column='OPINION_CREATE_USER')
    active_flag = models.BooleanField(default=True,db_column='OPINION_ACTIVE_FLAG')
    delete_flag = models.BooleanField(default=False,db_column='OPINION_DELETE_FLAG')
    delete_date = models.DateTimeField(null=True,blank=True,db_column='OPINION_DELETE_DATE')
    opinion_attached	 = models.ImageField(null=True,blank=True,upload_to=upload_to_snap_opinion_attach,db_column='OPINION_ATTACHED')
    delete_user =  models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='snap_opinion_deleted',db_column='OPINION_DELETE_USER')

    objects = AfrSnapActiveManager()
    all_objects = models.Manager()

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_SNAP_PER_OPINION'
        ordering = ['opinion_type__opinion_order']
        constraints = [
            models.UniqueConstraint(
                fields=['snap_id','opinion_type'],
                name='lagna_comm_snap_opinions',
                condition=Q(active_flag=True)
            )
        ]
        


class AfrSnapFinalDecition(models.Model):
    dec_id = models.BigAutoField(primary_key=True,db_column='DEC_ID')

    fin_dec	= models.ForeignKey(LagnaVoteOpinoin,on_delete=models.DO_NOTHING,null=False,related_name='final_decition',db_column='FIN_DEC')

    snap_id = models.ForeignKey(LagnaAfrSnapData,on_delete=models.DO_NOTHING,null=False,related_name='final_decition',db_column='SNAP_ID')
    committe_id = models.ForeignKey(Lagna,on_delete=models.DO_NOTHING,null=False,related_name='final_decition',db_column='COMMITTE_ID')
    comm_prnt_code = models.ForeignKey(ArmyCode,on_delete=models.DO_NOTHING,null=True,blank=True,db_column='COMM_PRNT_CODE')
    comm_type_id = models.ForeignKey(LagnaType,on_delete=models.DO_NOTHING,null=False,db_column='COMM_TYPE_ID')

    dec_notes = models.CharField(null=True,blank=True,max_length=2000)

    create_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,db_column='CREATE_USER')
    create_date = models.DateTimeField(auto_now_add=True)
    active_flag = models.BooleanField(default=True)

    delete_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='lagna_final_decition',db_column='DELETE_USER')
    delete_date = models.DateTimeField(null=True,blank=True)
    delete_flag = models.BooleanField(default=False)
    

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_SNAP_FINAL_DECISION'

        




class LagnaCommanderData(models.Model):
    commander_id = models.BigAutoField(primary_key=True)
    # snap_id	= models.ForeignKey(LagnaAfrSnapData,on_delete=models.DO_NOTHING,related_name='commanders',null=False,db_column='SNAP_ID')
    rank_id	= models.ForeignKey(Rank,on_delete=models.DO_NOTHING,related_name='commanders',null=False,blank=False,db_column='RANK_ID')
    comm_op_type = models.ForeignKey(CommanderJobType,on_delete=models.DO_NOTHING,null=False,db_column='COMM_OP_TYPE')
    comm_name = models.CharField(max_length=300,null=False)
    comm_job = models.CharField(max_length=100,null=False)
    comm_unit_date = models.DateTimeField(null=True,blank=True)
    telphone_no	= models.CharField(max_length=11,null=True,blank=True)
    active_flag = models.BooleanField(default=True)
    create_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,related_name='commander_creator',db_column='CREATE_USER')
    create_date	= models.DateTimeField(auto_now_add=True)
    delete_flag = models.BooleanField(default=False)
    delete_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,related_name='commander_creator_delete',blank=True,db_column='DELETE_USER')
    delete_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f'{self.comm_op_type} - {self.comm_job} - {self.comm_name}' 

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_COMMANDER_DATA'
        

class LagnaCommSnapDetail(models.Model):
    comm_snap_id = models.BigAutoField(primary_key=True)

    snap_id	 = models.ForeignKey(LagnaAfrSnapData,on_delete=models.DO_NOTHING,null=False,related_name='comm_snap_detail',db_column='SNAP_ID')
    commander_id = models.ForeignKey(LagnaCommanderData,on_delete=models.DO_NOTHING,null=False,related_name='comm_snap_detail',db_column='COMMANDER_ID')

    active_flag	= models.BooleanField(default=True)

    create_user	= models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='comm_snap_create',null=False,db_column='CREATE_USER')
    create_date	= models.DateTimeField(auto_now_add=True)

    delete_flag	= models.BooleanField(default=False)
    delete_user	= models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,db_column='DELETE_USER')
    delete_date	= models.DateTimeField(null=True,blank=True)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_COMM_SNAP_DETAIL'
        constraints = [
            models.UniqueConstraint(
                fields=['snap_id','commander_id'],
                name='lagna_comm_snap_detail',
                condition=Q(active_flag=True)
            )
        ]


class PonsConsType(models.Model):
    pons_cons_type_id = models.IntegerField(primary_key=True,null=False)
    pons_cons_name	= models.CharField(null=False,blank=False,max_length=500)

    def __str__(self):
        return self.pons_cons_name

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'PONS_CONS_TYPE'
        

class LagnaPersonPonsCons(models.Model):
    pons_cons_id = models.BigAutoField(primary_key=True)
    po_co_types = models.ForeignKey(PonsConsType,on_delete=models.DO_NOTHING,null=False,db_column='PO_CO_TYPES')
    po_co_notes	 = models.CharField(max_length=1000,null=False)
    comm_snap_id = models.ForeignKey(LagnaCommSnapDetail,on_delete=models.DO_NOTHING,null=False,related_name='person_cons_pons',db_column='COMM_SNAP_ID')

    active_flag = models.BooleanField(default=True)
    create_user	 = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,related_name='person_cons_create',db_column='CREATE_USER')
    create_date	 = models.DateTimeField(auto_now_add=True)

    delete_flag	 = models.BooleanField(default=False)
    delete_user	= models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='person_cons_delete',db_column='DELETE_USER')
    delete_date	= models.DateTimeField(null=True,blank=True)

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_PONS_CONS'


class LagnaPersonsOpinions(models.Model):
    opinion_id = models.BigAutoField(primary_key=True,null=False,db_column='OPINION_ID')

    person_id = models.ForeignKey(LagnaPersons,on_delete= models.DO_NOTHING,related_name='lagna_opinions',db_column='PERSON_ID')

    comm_snap_id = models.ForeignKey(LagnaCommSnapDetail,on_delete=models.DO_NOTHING,null=True,related_name='opinions',db_column='COMM_SNAP_ID')

    opinion_type = models.ForeignKey(OpinionType,on_delete=models.DO_NOTHING,related_name='lagna_person',db_column='OPINION_TYPE')
    opinion_code = models.ForeignKey(LagnaVoteOpinoin,on_delete=models.DO_NOTHING,related_name='lagna_person',db_column='OPINION_CODE')
    opinion_notes = models.CharField(null=True,blank=True,max_length=255)

    create_user	= models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='lagna_opinion',db_column='OPINION_CREATE_USER')
    create_date = models.DateTimeField(auto_now_add=True,null=False,db_column='OPINION_CREATE_DATE')
    active_flag	= models.BooleanField(default=True,db_column='OPINION_ACTIVE_FLAG')
    delete_flag	= models.BooleanField(default=False,db_column='OPINION_DELETE_FLAG')
    delete_date	= models.DateTimeField(null=True,blank=True,db_column='OPINION_DELETE_DATE')
    delete_user	= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='lagna_opinion_deleted',db_column='OPINION_DELETE_USER')
    opinion_attached = models.ImageField(null=True,blank=True)

    def delete(self,*args,**kwargs):
        self.active_flag=False
        self.delete_flag=True

        self.save()
    

    class Meta:
        managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
        db_table = 'AFR_COMM_PERSON_OPINION'
        ordering = ['person_id','opinion_type','opinion_code']



managed = getattr(settings , 'MANAGED_MIGRATIONS',False)
# print(managed)