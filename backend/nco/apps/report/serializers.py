from rest_framework import serializers
from apps.person.serializers import AfrPersonSerializerBasic,AfrPersonSerializerPhotoReport
from apps.person.models import AfrPerson
from apps.tanzem.models import ArmyCode
from .models import (
    PrntPhotoReport,
    UnitPhotoReport,
    AfrPhotoReport,
    LagnaAfrReport,
    LagnaAfrOpinionsReport,
)


#----------------------------- photo report ----------------------------------------

class PrntPhotoReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrntPhotoReport
        fields = '__all__'
        read_only_fields = [field.name for field in PrntPhotoReport._meta.fields]

class UnitPhotoReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitPhotoReport
        fields = '__all__'
        read_only_fields = [field.name for field in UnitPhotoReport._meta.fields]


class AfrPhotoReportSerializer(serializers.ModelSerializer):
    mil_ser =AfrPersonSerializerPhotoReport(read_only=True)

    class Meta:
        model = AfrPhotoReport
        fields = '__all__'
        read_only_fields = [field.name for field in AfrPhotoReport._meta.fields]


#----------------------------- lagna report ----------------------------------------

class LagnaAfrReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LagnaAfrReport
        fields = '__all__'
        read_only_fields = [field.name for field in LagnaAfrReport._meta.fields]


        

class LagnaAfrOpinionsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LagnaAfrOpinionsReport
        fields = ['opinion_code','opinion_name','vote_code','vote_name','total']
        read_only_fields = [field.name for field in LagnaAfrOpinionsReport._meta.fields]

class PrntArmyCodeOpinionReportSerializer(serializers.ModelSerializer):
    prnt_opinions_rep = serializers.SerializerMethodField()

    def get_prnt_opinions_rep(self,obj):
        spacific_code = self.context['spacific_code']
        army_code = self.context['army_code']
        opinions = obj.prnt_opinions_report.filter(army_code_id=army_code,spacific_code_id=spacific_code)
        return LagnaAfrOpinionsReportSerializer(opinions,many=True).data





    class Meta:
        model = ArmyCode
        fields = '__all__'
class ArmyCodeOpinionsReportSerializer(serializers.ModelSerializer):
    opinions_rep = serializers.SerializerMethodField(read_only=True)
    
    def get_opinions_rep(self,obj):
        spacific_code = self.context['spacific_code']
        # opinions =obj.opinions_report.filter(spacific_code_id=spacific_code)
        prnt_armies= ArmyCode.objects.filter(army_code__in = set(obj.opinions_report.filter(spacific_code_id=spacific_code).values_list('prnt_army_code',flat=True)))

        # return  LagnaAfrOpinionsReportSerializer(opinions,many=True).data
        return PrntArmyCodeOpinionReportSerializer(prnt_armies,many=True,context={'army_code':obj.army_code,'spacific_code':spacific_code}).data
    class Meta:
        model = ArmyCode
        fields = '__all__'
        