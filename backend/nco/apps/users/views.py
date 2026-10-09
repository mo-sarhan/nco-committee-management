from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import MethodNotAllowed,ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.contrib.auth.models import User
from apps.lagna.serializers import CreateLagnaSerializerBasic,LagnaTypeSpacificSerializerBasic,LagnaMemberSerializer
from apps.lagna.models import Lagna
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializerBasic,
            )
from .paginators import AccountCustomPaginators
from django.db import transaction


# Create your views here.


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class =CustomTokenObtainPairSerializer




# class ProfileViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']

#     def get_queryset(self):
#         user = self.request.user
#         profile = user.profile.all()
#         return profile





class AccountViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = AccountCustomPaginators
    serializer_class = UserSerializerBasic
    http_method_names = ['get']
    lookup_field = 'username'

    def get_queryset(self):
        user = self.request.user
        return [user]

    
    @transaction.atomic
    @action(detail=False , methods=['get'],permission_classes=[], url_path='comm')
    def get_invloved_comm_member(self,request,pk=None):
        try:
            user = self.request.user
            # committes = Lagna.objects.filter(lagna_type_spacific__member_user = user)
            temp  = []
            committes = user.lagna_member.filter(active_flag=True,delete_flag=False)
            for i in committes:
                temp.append(i.committe_code)
            page =self.paginate_queryset(temp)
            serializer =CreateLagnaSerializerBasic(page,many=True)
            
            return self.get_paginated_response(serializer.data)
        except  Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=400)
            


