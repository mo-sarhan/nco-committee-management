from rest_framework import serializers
from .models import (
    ArmyCode,
    Rank,
    Jobs
)



class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'

class ArmyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArmyCode
        fields = '__all__'
        read_only_fields = [field.name for field in ArmyCode._meta.fields]

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = ['rank_code','rank_name']
        read_only_fields = fields

