from rest_framework import serializers
import json
from django.contrib.auth.models import User
from utilts.converters import convert_date
from django.db import transaction
from django.db.models import Count,F,Value
from django.utils import timezone
from apps.users.serializers import UserSerializerBasic
from apps.report.services.generate_lagna_report import generate_lagna_report_by
from datetime import datetime,timedelta
from apps.tanzem.serializers import RankSerializer,ArmyCodeSerializer,JobsSerializer
from apps.tanzem.models import ArmyCode
from apps.report.serializers import LagnaAfrOpinionsReportSerializer,ArmyCodeOpinionsReportSerializer
from .services.get_or_create_snap import get_or_create_snap
from apps.tanzem.models import (
    ArmyParentChild,
)
from apps.person.serializers import (
                    AfrPersonSerializerBasic,
                    AfrPersonSerializerDetails,
                    AfrPersonLagnaSpacificSerializerBasic,
                    AfrPersonSerializerPhotoReport,
            )
            
from .models import (
    Lagna,
    OpinionType,
    LagnaPersonsOpinions,
    LagnaTypeSpacific,
    VoteType,
    LagnaMember,
    LagnaMemberType,
    LagnaPersons,
    LagnaPersonVotes,
    LagnaAfrStatus,
    LagnaType,
    LagnaCategory,
    LagnaVoteOpinoin,
    LagnaCommanderData,
    LagnaPersonReasons,
    LagnaPersonPonsCons,
    LagnaCommSnapDetail,
    LagnaAfrSnapData,
    AfrSnapFinalDecition,
    PonsConsType,
    CommanderJobType,
    AfrSnapOpinion,
    BenefitType,
)

class VoteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteType
        fields = '__all__'
        read_only_fields = ['active_flag','delete_flag']

class BenefitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitType
        fields = '__all__'



class LagnaVoteOpinoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = LagnaVoteOpinoin
        fields = ['opinion_name','opinion_code','committe_type_code']

class LagnaPersonReasonsSerializer (serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['descrption'] = convert_date(data['descrption'])
        return data

    class Meta:
        model = LagnaPersonReasons
        fields = '__all__'
        read_only_fields = ['reason_id','active_flag','delete_user','delete_date','delete_flag','create_user','create_date']

class LagnaPersonReasonsSerializerBasic (serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['descrption'] = convert_date(data['descrption'])
        return data

    class Meta:
        model = LagnaPersonReasons
        fields = ['reason_id','descrption','attach','create_date'] 
        read_only_fields = ['reason_id','active_flag','delete_user','delete_date','delete_flag','create_user','create_date']

class OpinionTypeSerializer(serializers.ModelSerializer):
    job = JobsSerializer(read_only=True)
    class Meta:
        model = OpinionType
        fields =('type_id','opinion_name','job') 
        read_only_fields = ('active_flag','delete_flag')



class LagnaTypeSerialzier(serializers.ModelSerializer):
    class Meta:
        model = LagnaType
        fields = '__all__'
        read_only_fields = ('delete_flag','create_date','active_flag')

class LagnaTypeSpacificSerializerInfo(serializers.ModelSerializer):
    # lagna_type = LagnaTypeSerialzier(read_only=True,source = 'committe_type')
    lagna_type_name = serializers.SerializerMethodField(read_only=True)
    range_dates = serializers.SerializerMethodField(read_only=True)

    def get_range_dates(self,obj):
        try:
            range_dates = [ waiting_date.date() for waiting_date in sorted(set(obj.lagna_persons.values_list('person_committe_date',flat=True))) if waiting_date != None]
            return range_dates
        except Exception as e:
            # print(e)
            return []

    def get_lagna_type_name(self,obj):
        return obj.committe_type.type_name

    class Meta:
        model = LagnaTypeSpacific
        fields = ('lagna_type_id','start_date','end_date','committe_type','committe_code','lagna_type_name','range_dates')
        read_only_fields = ('active_flag','delete_flag','create_date','create_user','create_date','delete_user','delete_date')

class LagnaTypeSpacificSerializerBasic(serializers.ModelSerializer):
    # lagna_type = LagnaTypeSerialzier(read_only=True,source = 'committe_type')
    lagna_type_name = serializers.SerializerMethodField(read_only=True)
    # range_dates = serializers.SerializerMethodField(read_only=True)

    # def get_range_dates(self,obj):
    #     try:
    #         # start_date = obj.committe_code.committe_start_date.date()
    #         # end_date = obj.committe_code.committe_end_date.date()
    #         # range_date = [
    #         #     (start_date + timedelta(days=i))
    #         #     for i in range((end_date-start_date).days + 1)
    #         # ]
    #         # range_date
    #         range_dates = [ waiting_date.date() for waiting_date in set(obj.lagna_persons.values_list('person_committe_date',flat=True)) if waiting_date != None]
    #         return range_dates
    #     except Exception as e:
    #         print(e)

    def get_lagna_type_name(self,obj):
        return obj.committe_type.type_name

    class Meta:
        model = LagnaTypeSpacific
        fields = ('lagna_type_id','start_date','end_date','committe_type','committe_code','lagna_type_name',
                #   'range_dates'
                  )
        read_only_fields = ('active_flag','delete_flag','create_date','create_user','create_date','delete_user','delete_date')

class LagnaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LagnaCategory
        fields='__all__'
        read_only_fields = ('delete_flag','active_flag','create_date')

class AfrSnapOpinionSerializer(serializers.ModelSerializer):
    opinion_type_data = OpinionTypeSerializer(read_only=True,source='opinion_type')
    opinion_data = LagnaVoteOpinoinSerializer(read_only=True,source='opinion_code')

    class Meta:
        model = AfrSnapOpinion
        fields = '__all__'
        read_only_fields = ('active_flag','delete_flag','delete_user','create_user','delete_date','create_date')



class LagnaTypeSpacificSerializerDetails(serializers.ModelSerializer):
    # lagna_type = LagnaTypeSerialzier(read_only=True,source = 'committe_type')
    lagna_type_name = serializers.SerializerMethodField(read_only=True)
    persons = serializers.SerializerMethodField(read_only=True,source='lagna_persons')

    def get_persons(self,obj):
        query = LagnaPersons.objects.filter(committe_type_code = obj,active_flag=True,delete_flag=False)
        serializer = LagnaPersonSerializerDetails(query,many=True)
        return serializer.data


    def get_lagna_type_name(self,obj):
        return obj.committe_type.type_name

    class Meta:
        model = LagnaTypeSpacific
        fields = ('lagna_type_id','start_date','end_date','committe_type','committe_code','lagna_type_name','persons')
        read_only_fields = ('active_flag','delete_flag','create_date','create_user','create_date','delete_user','delete_date')

class LagnaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LagnaCategory
        fields='__all__'
        read_only_fields = ('delete_flag','active_flag','create_date')


class CreateLagnaSerializerBasic(serializers.ModelSerializer):
    create_user = UserSerializerBasic(read_only=True,source='committe_create_user')
    # type = LagnaTypeSerialzier(read_only=True,source = 'committe_type')
    category = LagnaCategorySerializer(read_only=True,source = 'committe_category')
    lagna_types = LagnaTypeSpacificSerializerBasic(read_only=True,many=True,source = 'lagna_type_spacific')
    prnt_info = ArmyCodeSerializer(read_only=True,source='prnt_army_code')
    class Meta:
        model = Lagna
        fields = '__all__'
        read_only_fields = ('active_flag','delete_flag','committe_is_done','committe_create_date','committe_create_user','prnt_army_code')

class LagnaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LagnaAfrStatus
        fields = '__all__'



class LagnaPersonOpinionSerializer(serializers.ModelSerializer):
    opinion_type_data = OpinionTypeSerializer(read_only=True,source = 'opinion_type')
    opinion_data = LagnaVoteOpinoinSerializer(read_only=True,source='opinion_code')


    partial_update_fields = ['person_id']

    def validate(self, attrs):
        request = self.context.get('request')

        if request and request.method == 'PATCH':
            disallowed = set([field for field in attrs.keys() if field in self.partial_update_fields])
            if disallowed:
                raise serializers.ValidationError(
                    f'this fields can not be updated {self.partial_update_fields}'
                )

        return attrs


    class Meta:
        model = LagnaPersonsOpinions
        fields = '__all__'
        read_only_fields = ('active_flag','delete_flag','delete_user','delete_date','create_user','create_date')
class LagnaMemberTypeSerializer(serializers.ModelSerializer):
    vote_type_info =  VoteTypeSerializer(read_only=True,source='vote_type')
    class Meta:
        model = LagnaMemberType
        fields = ['vote_type','member_type_name','vote_type_info']

class LagnaMemberSerializer(serializers.ModelSerializer):
    user_info = UserSerializerBasic(read_only=True,source='member_user')
    type_info = LagnaMemberTypeSerializer(read_only=True,source='member_type')
    created_user =UserSerializerBasic(read_only=True,source='create_user') 
    class Meta:
        model = LagnaMember
        fields = '__all__'
        read_only_fields = [
            'delete_flag',
            'active_flag',
            'create_user',
            'create_date'
        ]

class LagnaPeronVotesSerializer(serializers.ModelSerializer):
    member = LagnaMemberSerializer(read_only=True,source='vote_member_id')
    vote_info =LagnaVoteOpinoinSerializer(read_only=True,source='vote')

    class Meta:
        model = LagnaPersonVotes
        fields = '__all__'
        read_only_fields = ('active_flag','delete_flag','create_date','vote_date','vote_id')

class AfrSnapFinalDecitionSerializer(serializers.ModelSerializer):
    pass

class LagnaPersonSerializerBasic(serializers.ModelSerializer):
    # lagna_status = LagnaStatusSerializer(read_only=True,source = 'committe_status_code')
    # review_user = UserSerializerBasic(read_only=True)
    committe_status_code = LagnaStatusSerializer(read_only=True)
    # lagna_opinoins = LagnaPersonOpinionSerializer(read_only=True,source = 'lagna_opinions')
    # opinions = serializers.SerializerMethodField(read_only=True)
    votes_info = serializers.SerializerMethodField(read_only=True)
    # votes_info_test = serializers.SerializerMethodField(read_only=True)
    final_decision = LagnaVoteOpinoinSerializer(read_only=True,source='committe_decision')
    # votes = LagnaPeronVotesSerializer (read_only=True,many=True)
    # person = AfrPersonSerializerBasic(read_only=True,source = 'mil_ser')
    person = AfrPersonLagnaSpacificSerializerBasic(read_only=True,source = 'mil_ser')
    # person =AfrPersonSerializerDetails(read_only=True,source = 'mil_ser')
    # final_decision = LagnaVoteOpinoinSerializer(read_only=True,source='committe_decision')
    # snap_info = serializers.SerializerMethodField(read_only=True) 

    # def get_snap_info(self,obj):
    #     afr_data = obj.mil_ser

    #     # user = self.context['request'].user
    #     user=None

    #     # Automated data from AfrPerson
    #     afr_data =obj.mil_ser 
        
    #     # Anchor Calculation
    #     mil_ser_id = afr_data.mil_ser
    #     comm_type_id = obj.committe_type_code.committe_type_id
    #     current_lagna = obj.committe_type_code.committe_code
    #     root_comm_id = current_lagna.main_committe_code_id or current_lagna.pk

    #     with transaction.atomic():
    #         # Get or Create the Shared Snap
    #         snap_instance, _ = LagnaAfrSnapData.objects.get_or_create(
    #             mil_ser_id=mil_ser_id,
    #             committe_type_id=comm_type_id,
    #             root_committe_id=root_comm_id,
    #             active_flag=True,
    #             defaults={
    #                 'unit_name': afr_data.unit_name, # Automated
    #                 'unit_code': afr_data.unit_code, # Automated
    #                 'army_code': afr_data.army_code, # Automated
    #                 'prnt_army_code_id': afr_data.prnt_army_code,
    #                 'degree_code': afr_data.degree_code,
    #                 'to_unit_date': afr_data.to_unit_date ,
    #                 'create_user': user
    #             }
    #         )
    #         return AfrSnapInfoSerializer(snap_instance).data


    def get_votes_info(self,obj):
        active_votes = obj.votes.filter(active_flag=True,delete_flag=False)
        serializer =LagnaPeronVotesSerializer(active_votes,many=True)
        return serializer.data


    def get_opinions(self,obj):
        query = LagnaPersonsOpinions.objects.filter(person_id = obj)
        serializer = LagnaPersonOpinionSerializer(query,many=True)
        return serializer.data

    
    class Meta:
        model = LagnaPersons
        fields = '__all__'
        read_only_fields = [
            'person_id',
            'add_user',
            'add_date',
            'delete_flag',
            'delete_user',
            'delete_date',
            'review_user',
            'review_date',
        ]

class LagnaPersonWithSnapSerializerBasic(serializers.ModelSerializer):
    # lagna_status = LagnaStatusSerializer(read_only=True,source = 'committe_status_code')
    # review_user = UserSerializerBasic(read_only=True)
    # root_committe=serializers.StringRelatedField(source='committe_type_code__committe_code__committe_name')
    root_committe_name = serializers.SerializerMethodField()
    comm_header = serializers.SerializerMethodField()
    committe_status_code = LagnaStatusSerializer(read_only=True)
    committe_type = serializers.SerializerMethodField(read_only=True)
    # lagna_opinoins = LagnaPersonOpinionSerializer(read_only=True,source = 'lagna_opinions')
    # opinions = serializers.SerializerMethodField(read_only=True)
    votes_info = serializers.SerializerMethodField(read_only=True)
    votes_info_test = serializers.SerializerMethodField(read_only=True)
    # votes = LagnaPeronVotesSerializer (read_only=True,many=True)
    # person = AfrPersonSerializerBasic(read_only=True,source = 'mil_ser')
    person = AfrPersonLagnaSpacificSerializerBasic(read_only=True,source = 'mil_ser')
    final_decision = LagnaVoteOpinoinSerializer(read_only=True,source='committe_decision')
    # person =AfrPersonSerializerDetails(read_only=True,source = 'mil_ser')
    # final_decision = LagnaVoteOpinoinSerializer(read_only=True,source='committe_decision')
    comm_total = serializers.SerializerMethodField(read_only=True)
    snap_info = serializers.SerializerMethodField(read_only=True) 
    comms_codes = serializers.SerializerMethodField(read_only=True)
    reasons_info = serializers.SerializerMethodField(read_only=True)

    def get_comm_header(self,obj):
        # user = obj.committe_type_code.members.filter(active_flag=True,delete_flag=False,member_type_id= 1).first()
        # print(obj.committe_type_code.members)
        main_lagna = obj.committe_type_code.committe_code
        member = main_lagna.members.filter(active_flag=True,delete_flag=False,member_type_id = 1).first()
        head_member = None
        if member:
            head_member = member.member_user

        # admin = User.objects.get(username='admin')

        serializer = UserSerializerBasic(head_member)
        return serializer.data


        


    def get_root_committe_name(self,obj):
        return obj.committe_type_code.committe_code.committe_name
    
    def get_reasons_info(self,obj):
        person_snap = get_or_create_snap(obj)
        
        active_reasons = person_snap.reasons.filter(active_flag=True,delete_flag=False)
        serializer = LagnaPersonReasonsSerializerBasic(active_reasons,many=True)
        return serializer.data

    def get_comm_total(self,obj):
        return obj.committe_type_code.lagna_persons.filter(active_flag=True,delete_flag=False).count()
    def get_comms_codes(self,obj):
        return {
            'committe_type':obj.committe_type_code_id,
            'committe_code':obj.committe_type_code.committe_code_id
        }
    
    def get_committe_type(self,obj):
        comm_type = obj.committe_type_code.committe_type
        return LagnaTypeSerialzier(comm_type).data

    def get_snap_info(self,obj):
        afr_data = obj.mil_ser

        # user = self.context['request'].user
        user=None

        # Automated data from AfrPerson
        afr_data =obj.mil_ser 
        
        # Anchor Calculation
        mil_ser_id = afr_data.mil_ser
        comm_type_id = obj.committe_type_code.committe_type_id
        current_lagna = obj.committe_type_code.committe_code
        root_comm_id = current_lagna.main_committe_code_id or current_lagna.pk

        with transaction.atomic():
            # Get or Create the Shared Snap
            snap_instance, _ = LagnaAfrSnapData.objects.get_or_create(
                mil_ser_id=mil_ser_id,
                committe_type_id=comm_type_id,
                root_committe_id=root_comm_id,
                active_flag=True,
                defaults={
                    'unit_name': afr_data.unit_name, # Automated
                    'unit_code': afr_data.unit_code, # Automated
                    'army_code_id': afr_data.army_code, # Automated
                    'prnt_army_code_id': afr_data.prnt_army_code,
                    'degree_code': afr_data.degree_code,
                    'to_unit_date': afr_data.to_unit_date ,
                    'create_user': user
                }
            )
            return AfrSnapInfoSerializer(snap_instance).data


    def get_votes_info(self,obj):
        active_votes = obj.votes.filter(active_flag=True,delete_flag=False)
        serializer =LagnaPeronVotesSerializer(active_votes,many=True)
        return serializer.data


    def get_opinions(self,obj):
        query = LagnaPersonsOpinions.objects.filter(person_id = obj)
        serializer = LagnaPersonOpinionSerializer(query,many=True)
        return serializer.data

    
    def get_votes_info_test(self,obj):
        active_votes = obj.votes.filter(active_flag=True,delete_flag=False,vote_member_id__member_type__vote_type_id=2).select_related('vote','vote_member_id__member_user')
        members_count=obj.committe_type_code.committe_code.members.filter(member_type__vote_type_id=2).count()
        # members_count=obj.committe_type_code.committe_code.members.count()
        total_votes = active_votes.count()
        # report_date=active_votes.annotate(total_votes=Count('pk')).values('vote__opinion_name','vote__opinion_code').annotate(vote_count=Count('pk',distinct=True)).annotate(percent=F('vote_count')/F('total_votes') * 100)
        # json_date = json.dumps(list(report_date.values('vote__opinion_name','vote__opinion_code','vote_count','percent')))
        
        opinions = {}
        for vote in active_votes:
            vote_id = vote.vote.opinion_code
            vote_name = vote.vote.opinion_name
            if vote_id not in opinions:
                opinions[vote_id] = {
                    'vote_name' : vote_name,
                    'vote_count':0,
                    'percent':0,
                    'voters':[]
                }  
            rank = vote.vote_member_id.member_user.profile.rank_code
            member_data = {
                'member_id':vote.vote_member_id_id,
                'username':vote.vote_member_id.member_user.username,
                'full_name':vote.vote_member_id.member_user.get_full_name(),
                'rank': rank.rank_name  if rank else None
            }
            opinions[vote_id]['voters'].append(member_data)
            opinions[vote_id]['vote_count'] +=1
            # opinions[vote_id]['percent'] += int(opinions[vote_id]['vote_count'] / total_votes * 100)
            opinions[vote_id]['percent'] = int(opinions[vote_id]['vote_count'] / total_votes * 100)


        

        return {'members_count':members_count,
                'total_votes':total_votes,
                'votes':list(opinions.values())}
        return list(opinions.values())
    class Meta:
        model = LagnaPersons
        fields = '__all__'
        read_only_fields = [
            'person_id',
            'add_user',
            'add_date',
            'delete_flag',
            'delete_user',
            'delete_date',
            'review_user',
            'review_date',
        ]



class AfrSnapFinalDecitionSerializer(serializers.ModelSerializer):
    committe = CreateLagnaSerializerBasic(read_only=True,source = 'committe_id')
    final_dec = LagnaVoteOpinoinSerializer(read_only=True,source = 'fin_dec')
    prnt_army = ArmyCodeSerializer(read_only=True,source = 'comm_prnt_code')
    committe_type = LagnaTypeSerialzier(read_only=True,source = 'comm_type_id')
    class Meta:
        model = AfrSnapFinalDecition
        fields = '__all__'

class AfrSnapInfoSerializer(serializers.ModelSerializer):
    opinions = AfrSnapOpinionSerializer(read_only=True,many=True)
    final_decition = AfrSnapFinalDecitionSerializer(read_only=True,many=True)
    class Meta:
        model = LagnaAfrSnapData
        fields = '__all__'
        read_only_fields = [field.name for field in LagnaAfrSnapData._meta.fields]

class LagnaPersonSerializerDetails(serializers.ModelSerializer):
    review_user = UserSerializerBasic(read_only=True)
    committe_status_code = LagnaStatusSerializer(read_only=True)
    opinions = serializers.SerializerMethodField(read_only=True)
    person =AfrPersonSerializerDetails(read_only=True,source = 'mil_ser')
    final_decision = LagnaVoteOpinoinSerializer(read_only=True,source='committe_decision')
    reasons_info = serializers.SerializerMethodField(read_only=True)
    comm_total = serializers.SerializerMethodField(read_only=True)
    snap_info = serializers.SerializerMethodField(read_only=True) 
    committe_type = serializers.SerializerMethodField(read_only=True)

    def get_comm_total(self,obj):
        return obj.committe_type_code.lagna_persons.filter(active_flag=True,delete_flag=False).count()

    def get_committe_type(self,obj):
        comm_type = obj.committe_type_code.committe_type
        return LagnaTypeSerialzier(comm_type).data


    def get_snap_info(self,obj):
        afr_data = obj.mil_ser

        # user = self.context['request'].user
        user=None

        # Automated data from AfrPerson
        afr_data =obj.mil_ser 
        
        # Anchor Calculation
        mil_ser_id =afr_data.mil_ser
        comm_type_id = obj.committe_type_code.committe_type_id
        current_lagna = obj.committe_type_code.committe_code
        root_comm_id = current_lagna.main_committe_code_id or current_lagna.pk


        with transaction.atomic():
            # Get or Create the Shared Snap
            snap_instance, _ = LagnaAfrSnapData.objects.get_or_create(
                mil_ser_id=mil_ser_id,
                committe_type_id=comm_type_id,
                root_committe_id=root_comm_id,
                active_flag=True,
                defaults={
                    'unit_name': afr_data.unit_name, # Automated
                    'unit_code': afr_data.unit_code, # Automated
                    'army_code_id': afr_data.army_code, # Automated
                    'prnt_army_code_id': afr_data.prnt_army_code,
                    'degree_code': afr_data.degree_code_id,
                    'to_unit_date': afr_data.to_unit_date ,
                    'create_user': user
                }
            )
            # print('snap_data :',snap_instance)
            return AfrSnapInfoSerializer(snap_instance).data

        
        

    def get_reasons_info(self,obj):
        person_snap = get_or_create_snap(obj)
        
        active_reasons = person_snap.reasons.filter(active_flag=True,delete_flag=False)
        serializer = LagnaPersonReasonsSerializerBasic(active_reasons,many=True)
        return serializer.data

    def get_opinions(self,obj):
        query = LagnaPersonsOpinions.objects.filter(person_id = obj)
        serializer = LagnaPersonOpinionSerializer(query,many=True)
        return serializer.data

    
    class Meta:
        model = LagnaPersons
        fields = '__all__'
        read_only_fields = [
            'person_id',
            'add_user',
            'add_date',
            'delete_flag',
            'delete_user',
            'delete_date',
            'review_user',
            'review_date',
            'active_flag'
        ]


class CommanderJobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommanderJobType
        fields = [field.name for field in CommanderJobType._meta.fields]


class PonsConsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PonsConsType
        fields = [field.name for field in PonsConsType._meta.fields]

#-------------------------- for snap data --------------------------------------
# Leaf 1: Pons and Cons
class PonsConsSerializer(serializers.ModelSerializer):
    po_co = PonsConsTypeSerializer(read_only=True,source='po_co_types')
    class Meta:
        model = LagnaPersonPonsCons
        fields = ['po_co_types', 'po_co_notes','po_co']

# Leaf 2: Opinions (Linked to the Stage/Person)
class OpinionSerializer(serializers.ModelSerializer):
    # We include the stage name (e.g., Sub-Lagna) for the GET response
    stage_name = serializers.CharField(source='person_id.committe_type_code.committe_code.committe_name', read_only=True)
    
    class Meta:
        model = LagnaPersonsOpinions
        fields = ['opinion_type', 'opinion_code', 'opinion_notes', 'stage_name', 'create_date']

# Leaf 3: Commanders
class CommanderSerializer(serializers.ModelSerializer):
    person_cons_pons = PonsConsSerializer(many=True,write_only=True,allow_null=True,required=False)
    # Note: A commander might have multiple opinions if added across stages
    # but based on your structure, it's a OneToOne per commander.
    opinions = OpinionSerializer(read_only=True) 
    rank_info = RankSerializer(read_only=True,source = 'rank_id')
    comm_op = CommanderJobTypeSerializer(read_only=True,source='comm_op_type')
    
    # For creation, we accept a single opinion object
    # write_opinion = OpinionSerializer(write_only=True, required=True)

    class Meta:
        model = LagnaCommanderData
        fields = [
            'commander_id', 'rank_id', 'comm_op_type', 'comm_name', 
            'comm_job', 'comm_unit_date', 'telphone_no', 
            'opinions', 'rank_info',
            'person_cons_pons','comm_op',
            # 'write_opinion',
        ]


class LagnaAfrSnapDataSerializer(serializers.ModelSerializer):
    person_id = serializers.PrimaryKeyRelatedField(queryset=LagnaPersons.objects.all(), write_only=True)
    commanders = CommanderSerializer(many=True,write_only=True)

    class Meta:
        model = LagnaAfrSnapData
        fields = ['person_id','snap_id','mil_ser', 'unit_code', 'army_code', 'prnt_army_code', 'degree_code', 'to_unit_date', 'commanders','benefit_id']
        read_only_fields = ['snap_id','opinions','unit_code','mil_ser', 'army_code', 'prnt_army_code', 'degree_code', 'to_unit_date']

    def create(self, validated_data):
        user = self.context['request'].user
        current_person = validated_data.pop('person_id')
        commanders_list = validated_data.pop('commanders')
        benefit = validated_data.pop('benefit_id',None)

        # Automated data from AfrPerson
        afr_data = current_person.mil_ser 
        
        # Anchor Calculation
        mil_ser_id = afr_data.mil_ser
        comm_type_id = current_person.committe_type_code.committe_type_id
        current_lagna = current_person.committe_type_code.committe_code
        root_comm_id = current_lagna.main_committe_code_id or current_lagna.pk

        with transaction.atomic():
            # Get or Create the Shared Snap
            snap_instance, snap_created = LagnaAfrSnapData.objects.get_or_create(
                mil_ser_id=mil_ser_id,
                committe_type_id=comm_type_id,
                root_committe_id=root_comm_id,
                active_flag=True,
                defaults={
                    'unit_name': afr_data.unit_name, # Automated
                    'unit_code': afr_data.unit_code, # Automated
                    'army_code_id': afr_data.army_code, # Automated
                    'prnt_army_code_id': afr_data.prnt_army_code,
                    'degree_code': afr_data.degree_code,
                    'to_unit_date': afr_data.to_unit_date ,
                    'benefit_id': benefit,
                    'create_user': user
                }
            )
            if not snap_created:
                snap_instance.benefit_id = benefit
                snap_instance.save(update_fields=['benefit_id'])

            for comm_item in commanders_list:
                pons_data = comm_item.pop('person_cons_pons', [])
                # opinion_data = comm_item.pop('write_opinion', None)

                commander_instance, comm_created = LagnaCommanderData.objects.get_or_create(
                    comm_op_type=comm_item.get('comm_op_type'),
                    comm_name = comm_item.get('comm_name'),
                    rank_id = comm_item.get('rank_id'),
                    comm_job = comm_item.get('comm_job'),
                    defaults={
                        'rank_id': comm_item.get('rank_id'),
                        'comm_name': comm_item.get('comm_name'),
                        'comm_unit_date': comm_item.get('comm_unit_date'),
                        'create_user': user
                    }
                )

                comm_snap_instance,comm_snap_created = LagnaCommSnapDetail.objects.get_or_create(
                    snap_id = snap_instance,
                    commander_id = commander_instance,
                    defaults={
                        'create_user': user,
                    }
                )

                if comm_snap_created:
                    if pons_data:
                        LagnaPersonPonsCons.objects.bulk_create([
                            LagnaPersonPonsCons(comm_snap_id=comm_snap_instance, create_user=user, **p) 
                            for p in pons_data
                        ])
                    # if opinion_data:
                    #     opinion_data['opinion_type'] = OpinionType.objects.get(comm_des_id=commander_instance.comm_op_type)
                    #     print(opinion_data)
                    #     LagnaPersonsOpinions.objects.create(
                    #         person_id=current_person,
                    #         comm_snap_id =comm_snap_instance,
                    #         create_user=user,
                    #         **opinion_data
                    #     )
        return snap_instance




class LagnaGetCommSnapSerializer(serializers.ModelSerializer):

    commanders =  CommanderSerializer(source='commander_id')
    opinions = LagnaPersonOpinionSerializer(many=True,read_only=True)
    pons_cons = PonsConsSerializer(many=True,read_only=True,source='person_cons_pons')

    class Meta:
        model = LagnaCommSnapDetail
        fields = '__all__'


# class AfrSnapFinalDecitionSerializer(serializers.ModelSerializer):
#     committe = CreateLagnaSerializerBasic(read_only=True,source = 'committe_id')
#     final_dec = LagnaVoteOpinoinSerializer(read_only=True,source = 'fin_dec')
#     prnt_army = ArmyCodeSerializer(read_only=True,source = 'comm_prnt_code')
#     committe_type = LagnaTypeSerialzier(read_only=True,source = 'comm_type_id')
#     class Meta:
#         model = AfrSnapFinalDecition
#         fields = '__all__'


class AfrSnapCustomReportInfoSerializer(serializers.ModelSerializer):
    benefit = BenefitTypeSerializer(read_only=True,source='benefit_id')
    opinions = AfrSnapOpinionSerializer(read_only=True,many=True)
    final_decition = AfrSnapFinalDecitionSerializer(read_only=True,many=True)
    commanders = serializers.SerializerMethodField(read_only=True)

    def get_commanders(self,obj):
        commander_list = []
        all_commander = obj.comm_snap_detail.all()
        for record in all_commander:
            commander = record.commander_id
            opinion_data=None
            # راي القائد المباشر
            if commander.comm_op_type_id == 1:
                opinion_type = commander.comm_op_type.opinion_type 
                opinion = obj.opinions.filter(opinion_type=opinion_type).first()
                if opinion:
                    opinion_data = opinion.opinion_code.opinion_name
            # رأي مدير السلاح
            if commander.comm_op_type_id == 3:
                # if obj.prnt_army_code_id == obj.army_code_id:
                    prnt_army_code = ArmyParentChild.objects.filter(child_code = obj.army_code_id).first()
                    # print(prnt_army_code)
                    if prnt_army_code :
                        final_decition = obj.final_decition.filter(comm_prnt_code_id = prnt_army_code.parent_code).first()
                        if final_decition:
                            opinion_data = final_decition.fin_dec.opinion_name

            # راي قائد التشكيل
            if commander.comm_op_type_id == 2:
                # if obj.prnt_army_code_id == obj.army_code_id:
                    prnt_army_code = ArmyParentChild.objects.filter(child_code = obj.prnt_army_code_id).first()
                    if prnt_army_code :
                        final_decition = obj.final_decition.filter(comm_prnt_code_id = prnt_army_code.parent_code).first()
                        if final_decition:
                            opinion_data = final_decition.fin_dec.opinion_name

            pons_cons_data = PonsConsSerializer(record.person_cons_pons.all(),many=True).data
            commander_obj = {
                'commander': CommanderSerializer(commander).data,
                'opinion': opinion_data,
                'pons_cons': pons_cons_data
            }
            commander_list.append(commander_obj)
        return commander_list




    class Meta:
        model = LagnaAfrSnapData
        fields = '__all__'
        read_only_fields = [field.name for field in LagnaAfrSnapData._meta.fields]

class LagnaPersonReportSerializer(serializers.ModelSerializer):

    opinions = serializers.SerializerMethodField(read_only=True)
    person = AfrPersonSerializerBasic(read_only=True,source='mil_ser')
    final_decision = serializers.StringRelatedField(read_only=True,source='committe_decision')

    def get_opinions(self,obj):
        snap_instance = get_or_create_snap(obj)
        opinions = snap_instance.opinions.all()
        serializer =AfrSnapOpinionSerializer(opinions,many=True)
        return serializer.data

    class Meta:
        model = LagnaPersons
        fields = ['opinions','person','final_decision']

class LagnaSpacificReportSerializer(serializers.ModelSerializer):
    root_committe_name = serializers.StringRelatedField(source='committe_code')
    army_report = serializers.SerializerMethodField(read_only=True)
    committe_type = LagnaTypeSerialzier(read_only=True)
    # decision_report = serializers.SerializerMethodField(read_only=True)
    # persons = LagnaPersonReportSerializer(many=True,source='lagna_persons')
    

    def get_army_report(self,obj):
        report_filter = {'spacific_code_id':obj.pk}
        return {
            # 'all' : generate_lagna_report_by(report_filter,group_by=['person_army_code','person_army_name','person_prnt_army_code','person_prnt_army_name','person_serv_army_code','person_serv_name']),
            'by_person_prnt_army' : generate_lagna_report_by(report_filter,group_by=['person_prnt_army_code'],output_fields=['person_prnt_army_name']),
            'by_person_army' : generate_lagna_report_by(report_filter,group_by=['person_army_code','person_army_name'],output_fields=['person_army_code','person_army_name']),
            'by_prnt_a_army': generate_lagna_report_by(report_filter,group_by=['person_prnt_army_code','person_army_name'],output_fields=['person_prnt_army_name','person_army_name']),
            'by_serv_army':generate_lagna_report_by(report_filter,group_by=['person_serv_army_code','person_serv_name'],output_fields=['person_serv_name']),
            'all' : generate_lagna_report_by(report_filter,group_by=['person_army_code','person_army_name','person_prnt_army_code','person_prnt_army_name','person_serv_army_code','person_serv_name']),
        }
    
    def get_decision_report(self,obj):
        persons = obj.lagna_persons.filter(active_flag=True,delete_flag=False)
        serializer = LagnaPersonSerializerBasic(persons,many=True)
        return serializer.data

    class Meta:
        model = LagnaTypeSpacific
        fields = ['lagna_type_id','committe_type','root_committe_name','army_report']

class LagnaSpacificOpinionsReportSerializer(serializers.ModelSerializer):
    root_committe_name = serializers.StringRelatedField(source='committe_code')
    committe_type = LagnaTypeSerialzier(read_only=True)
    opinions_report = serializers.SerializerMethodField()

    def get_opinions_report(self,obj):
        armies = ArmyCode.objects.filter(army_code__in = set(obj.opinions_report.values_list('army_code',flat=True)))
        serializer = ArmyCodeOpinionsReportSerializer(armies,many=True,context={'spacific_code':obj.pk})
        return serializer.data

    class Meta:
        model = LagnaTypeSpacific
        fields = ['lagna_type_id','committe_type','root_committe_name','opinions_report']


class LagnaReportSerilaizer(serializers.ModelSerializer):

    # report = serializers.SerializerMethodField(read_only=True)
    lagna_report = LagnaSpacificReportSerializer(many=True,source='lagna_type_spacific',read_only=True)

    def get_report(self,obj):
        report_filter = {'committe_code':obj.pk}
        spacific_code = self.context.get('spacific_code')
        # print('type_code :',spacific_code)
        if spacific_code:
            report_filter['spacific_code_id']=spacific_code
        return {
            'all' : generate_lagna_report_by(report_filter,group_by=[],output_fields=[]),
            'by_type_name' : generate_lagna_report_by(report_filter,group_by=['committe_name','type_code','type_name'],output_fields=['type_code','type_name']),
            'by_person_prnt_army' : generate_lagna_report_by(report_filter,group_by=['committe_name','type_name','person_prnt_army_code'],output_fields=['type_name','person_prnt_army_name']),
            'by_person_army' : generate_lagna_report_by(report_filter,group_by=['type_code','committe_name','type_name','person_army_code','person_army_name'],output_fields=['type_name','person_army_code','person_army_name']),
            'by_prnt_a_army': generate_lagna_report_by(report_filter,group_by=['type_code','committe_name','person_prnt_army_code','person_army_name'],output_fields=['type_name','person_prnt_army_name','person_army_name']),
            'by_serv_army':generate_lagna_report_by(report_filter,group_by=['type_code','committe_name','type_name','person_serv_army_code','person_serv_name'],output_fields=['type_name','person_serv_name']),
            'final_distions':generate_lagna_report_by(report_filter,group_by=['committe_name','committe_code','spacific_code__lagna_persons__committe_decision__opinion_name','type_name'],output_fields=['type_name','spacific_code__lagna_persons__mil_ser__mil_no','spacific_code__lagna_persons__mil_ser__person_name','spacific_code__lagna_persons__committe_decision__opinion_name'])
        }

    class Meta:
        model = Lagna
        fields = '__all__'


class LagnaPersonPhotoReportSerializer(serializers.ModelSerializer):
    person = AfrPersonSerializerPhotoReport(source='mil_ser')
    class Meta:
        model = LagnaPersons
        fields = ['mil_ser','person']