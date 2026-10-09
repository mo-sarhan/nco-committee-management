from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import AfrPersonSerializerBasic,AfrPersonSerializerDetails
from .services.get_person_services import get_persons,get_person_details
from .paginator import CustomPaginator
from .models import AfrPerson
from apps.tanzem.models import ArmyParentChild
from django.db import transaction,models
from apps.lagna.models import LagnaTypeSpacific
from rest_framework import serializers
# from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from apps.photos.serializers import PhotoInfoSerializerBasic
from django.core.cache import cache
from .mixins import (
    AfrPersonUnitMixin,
    AfrPersonPhotosMixin,
    AfrPsychologicalReportMixin,
    AfrSecurityMixin,
)


class HelloSerializer(serializers.Serializer):
    message = serializers.CharField()

class HelloSerializerGet(serializers.Serializer):
    input_value= serializers.IntegerField()


@swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'person_name',
                openapi.IN_QUERY,
                description='search by name',
                type=openapi.TYPE_STRING,
                default='محمد'
            )
        ]  
      )

class AfrPersonView(AfrSecurityMixin,AfrPsychologicalReportMixin,AfrPersonPhotosMixin,AfrPersonUnitMixin,ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AfrPerson.objects.all()
    pagination_class = CustomPaginator
    # http_method_names = ['get']
    #----------------------------------------
    #      enable it after enable cache in upload photo or any variable data
    #----------------------------------------
    # def get_cache_key(self,pk=None):
    #     basic = bool(self.request.query_params.get('basic'))
    #     temp = 'basic' if basic else None
    #     if pk:
    #         return f'mil_ser{pk}_{temp}'
    #     else:
    #         return pk


    # def retrieve(self, request, *args, **kwargs):
    #     cache_key = self.get_cache_key(pk=kwargs['pk'])
    #     print(cache_key)
    #     data = cache.get(cache_key)
    #     print(data)
    #     if data:
    #         return Response(data,status=200)
        
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     cache.set(cache_key,serializer.data,60)
    #     return Response(serializer.data,status=200)



    def get_queryset(self):
        user = self.request.user
        filter_keys = self.request.query_params
        model_fields = set(field.name for field in AfrPerson._meta.fields)
        # final_field = set(field for field in  filter_keys.keys() if field in model_keys  )

        # stud_condition= ~Q(degree_code=0)
        stud_condition= Q()
        lagna_conditioin  = Q()
        can_see_condition = Q()
        filter_condition  = Q()

        if user.is_superuser or user.has_perm('person.can_see_all_people'):
            can_see_condition = Q()
        else:
            if hasattr(user,'profile'):
                can_see_condition = Q(prnt_army_code = user.profile.prnt_army_code_id)
                child_codes = set(ArmyParentChild.objects.filter(parent_code = user.profile.prnt_army_code_id).values_list('child_code',flat=True))
                army_condition=Q()
                if bool(filter_keys.get('prnt_army')):
                    can_see_condition = Q(prnt_army_code = user.profile.prnt_army_code_id)|Q(army_code = user.profile.prnt_army_code_id)
                    army_condition = Q(army_code__in = child_codes)
                    # print(can_see_condition)


                # print(child_codes)
                child_condition = Q(prnt_army_code__in =child_codes)
                # print('child_condition',child_condition)
                # print('can see condition',can_see_condition)
                can_see_condition = can_see_condition|child_condition |army_condition
                # print('can see condition 2',can_see_condition)
            else:
                return AfrPerson.objects.none()

        lagna_spacific_id = filter_keys.get('lagna_specific_id')
        # print(filter_keys)
        # print('lsi',lagna_spacific_id)
        if lagna_spacific_id:
            lagna_spacific = LagnaTypeSpacific.objects.get(pk=lagna_spacific_id,active_flag=True,delete_flag=False)
            # print('lagna_spacific',lagna_spacific)
            persons_mil_ser= set(lagna_spacific.lagna_persons.filter(active_flag=True,delete_flag=False).values_list('mil_ser',flat=True))
            # print(persons_mil_ser)
            lagna_conditioin = ~Q(mil_ser__in = persons_mil_ser)

        for field_name,field_value in filter_keys.items():
            if field_name in model_fields and field_value:
                field = AfrPerson._meta.get_field(field_name)
                if isinstance(field,models.CharField):
                    filter_condition &=Q(**{f'{field_name}__icontains':field_value})
                elif isinstance(field,models.IntegerField):
                    filter_condition &=Q(**{f'{field_name}__exact':field_value})
        

        
        # if not user.is_superuser:
        #     if hasattr(user,'profile'):
        #         # every user can see its prnt_army_code 
        #         temp_condition = Q()
        #         if bool(filter_keys.get('prnt_army')):
        #             temp_condition = Q(Q(prnt_army_code = user.profile.prnt_army_code_id) | Q(army_code = user.profile.prnt_army_code_id))
        #             lagna_spacific_id = filter_keys.get('lagna_spacific_id')
        #             lagna_spacific = LagnaTypeSpacific.objects.get(pk=lagna_spacific_id,active_flag=True,delete_flag=False)
        #             persons_mil_ser= set(lagna_spacific.persons.filter(active_flag=True,delete_flag=False).values_list('mil_ser_id',flat=True))
        #             lagna_conditioin &= ~Q(mil_ser__in = persons_mil_ser)

                
        #         else:
        #             temp_condition = Q(prnt_army_code = user.profile.prnt_army_code_id)
        #         # every user can see its
        #         child_codes = set(ArmyParentChild.objects.filter(parent_code = user.profile.prnt_army_code_id).values_list('child_code',flat=True))
        #         print(child_codes)
        #         child_condition = Q(prnt_army_code__in =child_codes)
        #         condition &=Q(Q(temp_condition)|Q(child_condition))

        #     else:
        #         return AfrPerson.objects.none()

        # for field_name,field_value in filter_keys.items():
        #     if field_name in model_fields and field_value:
        #         field = AfrPerson._meta.get_field(field_name)
        #         if isinstance(field,models.CharField):
        #             condition &=Q(**{f'{field_name}__icontains':field_value})
        #         elif isinstance(field,models.IntegerField):
        #             condition &=Q(**{f'{field_name}__exact':field_value})
        
        main_condition = Q(stud_condition&lagna_conditioin&can_see_condition&filter_condition)
        # print('main_condition',main_condition)
        return AfrPerson.objects.filter(main_condition)
        



    def get_serializer_class(self):
        basic = bool(self.request.query_params.get('basic'))
        if basic :
            return AfrPersonSerializerBasic
        if self.action == 'list':
            return AfrPersonSerializerBasic
        return AfrPersonSerializerDetails
