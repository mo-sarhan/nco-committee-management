from rest_framework import serializers
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from apps.photos.models import PhotoInfo
from apps.photos.serializers import PhotoInfoSerializerBasic,PhotoInfoSerializer
from utilts.converters import convert_to_arabic,convert_date
from apps.person.models import (
    AfrPerson,
    AfrVacation,
    AfrEducation,
    AfrUnits,
    AfrPunishment,
    Family,
    FamilyStatistic,
    MedicalLagnaResultLookUp,
    MedicalHistory,
    PersonEffecincy,
    PersonEffecincyL3Y,
    PersonEffecincyAvg,
    AfrTagdedHistroy,
    PunishmentStatistics,
    AfrPsychologicalReport,
    AfrTravel,
    AfrSecuritySituation,
)


class AfrVacationSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['start_date'] =convert_to_arabic(data['start_date'])
        # data['end_date'] =convert_to_arabic(data['end_date'])
        data['notes'] =convert_date(data['notes'])
        return data
    class Meta:
        model = AfrVacation
        fields = '__all__'

class AfrSecuritySituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfrSecuritySituation
        fields = '__all__'
        read_only_fields = ['create_user','delete_user','active_flag','delete_flag','create_date','delete_date']
        

class AfrPsychologigcalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfrPsychologicalReport
        fields = '__all__'
        read_only_fields = ['create_user','delete_user','active_flag','delete_flag','create_date','delete_date']


class AfrTravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfrTravel
        fields = '__all__'

class AfrEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfrEducation
        fields = '__all__'

class AfrUnitsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['unit_name'] = convert_to_arabic(data['unit_name'])
        return data

    class Meta:
        model = AfrUnits
        fields = '__all__'

class AfrPunishmentSerializer(serializers.ModelSerializer):
    punish_period_type = serializers.SerializerMethodField(read_only=True)


    def get_punish_period_type(self,obj):
        period_types  = {
            1: 'يوم',
            30:'شهر',
            360:'سنة',
            0:'',
            None:''
        }
        return period_types.get(obj.punish_type,'')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['notes'] = convert_date(data['notes'])
        data['punishment_name'] = convert_to_arabic(data['punishment_name'])
        return data

    
    class Meta:
        model = AfrPunishment
        fields = '__all__'

class FamilySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['notes'] = convert_date(data['notes'])
        return data

    class Meta:
        model = Family
        fields = '__all__'

class FamilyStatisticSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['father_job'] = convert_date(data['father_job'])
        data['mother_job'] = convert_date(data['mother_job'])
        data['whife_job'] = convert_date(data['whife_job'])
        return data
    class Meta:
        model = FamilyStatistic
        fields = '__all__'

class MedicalLagnaResultLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalLagnaResultLookUp
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    # result = MedicalLagnaResultLookUpSerializer(read_only=True,source = 'lagna_result')
    result = serializers.StringRelatedField(source='lagna_result')
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class PersonEffecincySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonEffecincy
        fields = '__all__'

class PersonEffecincyL3YSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonEffecincyL3Y
        fields = '__all__'
class PersonEffecincyAvgSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonEffecincyAvg
        fields = '__all__'
class PersonTagdedHistorySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['nashra_name'] =convert_to_arabic(data['nashra_name'])
        return data
    class Meta:
        model = AfrTagdedHistroy
        fields = '__all__'

class PunishmentStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PunishmentStatistics
        fields = '__all__'


class AfrPersonSerializerBasic(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField(read_only=True)
    def get_photos(self,obj):
        query=obj.photos.filter(active_flag=True)
        # serializer =PhotoInfoSerializerBasic(query,many=True)
        serializer =PhotoInfoSerializerBasic(query,many=True)
        return serializer.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['person_adress'] = convert_to_arabic(data['person_adress'])
        data['unit_name'] = convert_to_arabic(data['unit_name'])
        data['army_job_name'] = convert_to_arabic(data['army_job_name'])
        return data
    class Meta:
        model = AfrPerson
        fields = '__all__'

class AfrPersonLagnaSpacificSerializerBasic(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['unit_name'] = convert_to_arabic(data['unit_name'])
        return data
    class Meta:
        model = AfrPerson
        fields = ['mil_ser','mil_no','person_name','unit_name','unit_code','degree_name','degree_code','army_name','prnt_army_name']


class AfrPersonSerializerDetails(serializers.ModelSerializer):
    education = AfrEducationSerializer(many = True,read_only=True)
    units  = AfrUnitsSerializer(many = True,read_only=True)
    # family= FamilySerializer(many = True,read_only=True)
    family_statistic = FamilyStatisticSerializer(many=True,read_only=True)
    medical_history  = MedicalHistorySerializer(many = True,read_only=True)
    effecincy = PersonEffecincySerializer(many = True,read_only=True)
    effecincy_l3y = PersonEffecincyL3YSerializer(many=True,read_only=True,source = 'person_effecincy_l3y')
    effecincy_avg = PersonEffecincyAvgSerializer(many=True,read_only=True,source = 'person_effecincy_avg')
    # tagded_histroy = PersonTagdedHistorySerializer(many=True,source='tagded_history',read_only=True)
    tagded_history_info = serializers.SerializerMethodField()
    person_punishment = AfrPunishmentSerializer(many=True,read_only=True)
    punishment_statistics  = PunishmentStatisticsSerializer(many = True ,source='statistics',read_only=True)
    travel = AfrTravelSerializer(many=True,read_only=True)
    security = AfrSecuritySituationSerializer(many=True,read_only=True)
    psycholgical_report = serializers.SerializerMethodField(read_only=True)
    photos = serializers.SerializerMethodField(read_only=True)
    weight_diff = serializers.SerializerMethodField(read_only=True)
    family_info = serializers.SerializerMethodField(read_only=True)
    vacation = AfrVacationSerializer(many=True,read_only=True)

    def get_tagded_history_info(self,obj):
        tagded = obj.tagded_history.filter(upgra=2)
        tarky = obj.tagded_history.filter(upgra=1)

        return {
            'tagded':PersonTagdedHistorySerializer(tagded,many=True).data,
            'tarky':PersonTagdedHistorySerializer(tarky,many=True).data
        }

    def get_family_info(self,obj):
        family=obj.family
        ordering = ['kawmy_number','relation_degree_code']

        family_details={
            'current_marrige':FamilySerializer(family.filter(Q(relation_degree_code__in=[1,15],onlife_or_not=True)).order_by(*ordering),many=True).data,
            'prev_marrige':FamilySerializer(family.filter(Q(relation_degree_code__in=[16])|Q(relation_degree_code__in=[1,15],onlife_or_not=False)),many=True).data,
            'father':FamilySerializer(family.filter(relation_degree_code__in=[3]),many=True).data,
            'mother':FamilySerializer(family.filter(relation_degree_code__in=[4]),many=True).data,
            'children':FamilySerializer(family.filter(relation_degree_code__in=[2,7]),many=True).data,
            'sons':FamilySerializer(family.filter(relation_degree_code__in=[2]),many=True).data,
            'doughter':FamilySerializer(family.filter(relation_degree_code__in=[7]),many=True).data,
            'bro_sis':FamilySerializer(family.filter(relation_degree_code__in=[5,6]).order_by('birth_year'),many=True).data,
            'relatives':FamilySerializer(family.filter(relation_degree_code__in=[8,9,10,11]),many=True).data
        }
        return family_details



        
    


    def get_psycholgical_report(self,obj):
        query = obj.psycholgical_report.filter(active_flag=True,delete_flag=False)
        serializer = AfrPsychologigcalReportSerializer(query,many=True)
        return serializer.data
    

    def get_photos(self,obj):
        query=obj.photos.filter(active_flag=True,delete_flag=False)
        serializer = PhotoInfoSerializerBasic(query,many=True)
        return serializer.data

    def get_weight_diff(self,obj):
        hight = obj.length
        weight = obj.weight
        weight_diff = 'لايكن'
        if hight and weight:
            if (weight + 100) - (hight * -1) > 0:
                weight_diff = weight + 100 - (hight * - 1)
            else:
                weight + 100 - hight
        return weight_diff

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['person_adress'] = convert_to_arabic(data['person_adress'])
        data['unit_name'] = convert_to_arabic(data['unit_name'])
        data['army_job_name'] = convert_to_arabic(data['army_job_name'])
        return data
        

    class Meta:
        model = AfrPerson
        fields = '__all__'


class AfrPersonSerializerPhotoReport(serializers.ModelSerializer):
    # photos = PhotoInfoSerializer(read_only=True,many=True)
    photos = serializers.SerializerMethodField(read_only=True)

    def get_photos(self,obj):
        photos = obj.photos.filter(active_flag=True,delete_flag=False)
        serializer =PhotoInfoSerializer(photos,many=True)
        return serializer.data


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['unit_name'] = convert_to_arabic(data['unit_name'])
        return data
    
    class Meta:
        model = AfrPerson
        fields = ['mil_ser','mil_no','degree_name','person_name','army_name','army_code','unit_name','unit_code','marital_state_name','prnt_army_name','prnt_army_code','person_sex_name','photos','marital_state_name']


