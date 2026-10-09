from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from apps.tanzem.serializers import RankSerializer,JobsSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer






class ProfileSerializer(serializers.ModelSerializer):
    rank = RankSerializer(read_only=True,source='rank_code')
    job = serializers.StringRelatedField()
    job_info = JobsSerializer(source='job')
    class Meta:
        model = Profile
        fields = ('mil_no','rank_name','job','rank','job_info')

class UserSerializerBasic(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','last_login','profile')
        read_only_fields = fields

class CreateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('username','first_name,','last_name','profile','password')

        extra_kwargs = {
            'password':{'write_only':True}
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    # def get_token_for_user(user):
    #     token = 

    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_superuser'] = self.user.is_superuser
        data['role'] = list(self.user.groups.values_list('name',flat=True))
        data['info'] = UserSerializerBasic(self.user).data
        return data