from django.db import transaction
from rest_framework.exceptions import ValidationError
from datetime import datetime,timedelta
from django.db.models import Q
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.viewsets import ModelViewSet
from apps.person.paginator import CustomPaginator
from apps.tanzem.models import ArmyParentChild
from rest_framework.permissions import IsAuthenticated
from apps.tanzem.models import ArmyCode
from apps.tanzem.serializers import ArmyCodeSerializer
from .permissions import (
    IsOwnerOrSuperUser,
    AllowToAddOrEditPerson,
)
from .serializers import (
    CreateLagnaSerializerBasic,
    LagnaTypeSerialzier,
    LagnaCategorySerializer,
    LagnaVoteOpinoinSerializer,
    LagnaPersonSerializerDetails,
    LagnaPersonSerializerBasic,
    LagnaMemberSerializer,
    LagnaPersonOpinionSerializer,
    LagnaTypeSpacificSerializerBasic,
     OpinionTypeSerializer,
     PonsConsTypeSerializer,
     BenefitTypeSerializer,
     CommanderJobTypeSerializer,
     LagnaStatusSerializer,

    )
from .models import (
    Lagna,
    LagnaCategory,
    LagnaPersonsOpinions,
    LagnaType,
    LagnaVoteOpinoin,
    LagnaTypeSpacific,
    LagnaPersons,
    LagnaAfrStatus,
    LagnaMember,
    OpinionType,
    PonsConsType,
    BenefitType,
    CommanderJobType,
    )

from .mixins import (
    AddPersonMixin,

    GetVoteMemberMixin,

    LagnaPersonOpinionMixin,

    LagnaSpacificMixin,

    LagnaSpacificPersonMixin,
    LagnaSpacificMemberMixin,
    LagnaPersonStatusMixin,
    LagnaShowMixin,
    LagnaReportMixin,
    LagnaPersonReasonsMixin,
    SnapDataMixin,

)


class LagnaViewSet(
    SnapDataMixin,
    LagnaReportMixin,
    LagnaShowMixin,
    LagnaPersonReasonsMixin,
    LagnaPersonStatusMixin,
    LagnaSpacificMemberMixin,
    LagnaSpacificPersonMixin,
    LagnaSpacificMixin,
    ModelViewSet,
    ):
    permission_classes = [IsAuthenticated]
    queryset = Lagna.objects.all()
    serializer_class = CreateLagnaSerializerBasic
    pagination_class = CustomPaginator
    http_method_names = ['get','post','patch','delete']

    # MODEl_FIELDS = 

    def get_queryset(self):
        # return Lagna.objects.all()

        queryset = Lagna.objects.prefetch_related(
            'main_committe_code',
            'committe_create_user',
            'prnt_army_code',
            'committe_category'
        )



        user = self.request.user
        # filter_keys = self.request.query_params
        params = self.request.query_params
        # final_field = set(field for field in  filter_keys.keys() if field in model_keys  )

        # condition = Q(delete_flag=False,active_flag=True)
        # if not user.is_superuser:
        #     if not hasattr(user,'profile') or not user.profile.prnt_army_code_id:
        #         return Lagna.objects.none()
        #     parent = ArmyParentChild.objects.filter(child_code = user.profile.prnt_army_code_id).first()
            
        #     if parent:
        #         queryset=queryset.filter( Q(prnt_army_code_id =  parent.parent_code)|Q(prnt_army_code_id =user.profile.prnt_army_code_id))
        #     else:
        #         queryset=queryset.filter(prnt_army_code_id =user.profile.prnt_army_code_id)



        # model_fields = set(field.name for field in Lagna._meta.fields)
        # for field_name,field_value in filter_keys.items():
        #     if field_name in model_fields and field_value:
        #         field = Lagna._meta.get_field(field_name)
        #         if isinstance(field,models.CharField):
        #             condition &=Q(**{f'{field_name}__icontains':field_value})
        #         elif isinstance(field,models.ForeignKey):
        #             condition &=Q(**{f'{field_name}':field_value})
        #         elif isinstance(field,models.IntegerField):
        #             condition &=Q(**{f'{field_name}__exact':field_value})
        parent = None
        if hasattr(user, "profile") and user.profile.prnt_army_code_id:
            user_army_code = user.profile.prnt_army_code_id

            parent = ArmyParentChild.objects.filter(
                child_code=user_army_code
            ).first()
        if not user.is_superuser:

                if not hasattr(user, "profile") or not user.profile.prnt_army_code_id:
                    queryset=queryset.filter(members__member_user=user)
                    # return Lagna.objects.none()

                
                elif user.has_perm('lagna.can_see_main_lagna'):
                    queryset=queryset.filter( Q(prnt_army_code_id =  parent.parent_code)|Q(prnt_army_code_id =user.profile.prnt_army_code_id)|Q(committe_category_id=2))

                # elif user.has_perm('lagna.member_lagna'):
                    # queryset=queryset.filter(committe_category_id=2)
                elif parent:
                    queryset = queryset.filter(
                        Q(prnt_army_code_id=user_army_code) |
                        Q(prnt_army_code_id=parent.parent_code)
                    )
                else:
                    queryset = queryset.filter(
                        prnt_army_code_id=user_army_code
                    )

    # ---------------------------------
    # Dynamic Filtering (Safe Version)
    # ---------------------------------
        model_fields = {
            field.name: field
            for field in Lagna._meta.fields
        }

        for field_name, field_value in params.items():

            if not field_value:
                continue

            field = model_fields.get(field_name)

            if not field:
                continue

            if isinstance(field, models.CharField):
                queryset = queryset.filter(
                    **{f"{field_name}__icontains": field_value}
                )

            elif isinstance(field, models.IntegerField):
                queryset = queryset.filter(
                    **{f"{field_name}": field_value}
                )

            elif isinstance(field, models.ForeignKey):
                queryset = queryset.filter(
                    **{f"{field_name}_id": field_value}
                )
        # return Lagna.objects.all()
        return queryset

        # return base_queryset.filter(condition)
        # return Lagna.objects.filter(condition)
    
    @transaction.atomic
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    @transaction.atomic
    def perform_create(self, serializer):
        try:
            serializer.save(committe_create_user = self.request.user,prnt_army_code = self.request.user.profile.prnt_army_code)
        except Exception as e:
            transaction.set_rollback(True)
            raise ValidationError(str(e))

    @transaction.atomic
    @action(detail=False, methods=['get'] , url_path='get-lagna-type')
    def get_lagna_type(self,request):
        try:
            query=LagnaType.objects.all()
            serializer = LagnaTypeSerialzier(query,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=False, methods=['get'] , url_path='get-lagna-category')
    def get_lagna_category(self,request):
        try:
            query=LagnaCategory.objects.all()
            serializer = LagnaCategorySerializer(query,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    
    @transaction.atomic
    @action(detail=False, methods=['get'] , url_path='main')
    def get_main_lagna(self,request):
        try:
            query = Lagna.objects.filter(committe_category=2)
            serializer =  CreateLagnaSerializerBasic(query,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


class ConsPonsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PonsConsTypeSerializer
    queryset = PonsConsType.objects.all()
    http_method_names = ['get']



class LagnaPersonsViewSet(
    
    LagnaPersonOpinionMixin,

    ModelViewSet
    ):
    serializer_class = LagnaPersonSerializerBasic
    permission_classes = [IsAuthenticated,AllowToAddOrEditPerson]
    pagination_class = CustomPaginator
    queryset = LagnaPersons.objects.all()

    def get_queryset(self):
        try:
            user = self.request.user
            qs = LagnaPersons.objects.filter(delete_flag=False)
            return qs
        except Exception as e:
            return LagnaPersons.objects.none()


    @transaction.atomic
    def perform_create(self, serializer):
        try:
            serializer.save(add_user = self.request.user)
        except Exception as e:
            transaction.set_rollback(True)
            raise ValidationError({'error':str(e)})


    # Soft delete single record
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete_flag = True
        instance.delete_user = request.user
        instance.delete_date = timezone.now()
        instance.save()
        return Response({"message": "Soft deleted"}, status=200)



class LagnaMemberViewSet(
    GetVoteMemberMixin,
    ModelViewSet
    ):
    pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated]
    serializer_class = LagnaMemberSerializer


    def get_queryset(self):
        return LagnaMember.objects.filter(delete_flag=False)

    def perform_create(self, serializer):
        try:
            serializer.save(create_user = self.request.user)
        except Exception as e:
            raise ValidationError({'error':str(e)})

    @transaction.atomic
    def perform_create(self, serializer):
        try:
            serializer.save(create_user=self.request.user)
        except Exception as e:
            raise ValidationError({'error':str(e)})

            
class LagnaAfrStatusViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LagnaStatusSerializer
    queryset = LagnaAfrStatus.objects.all()
    http_method_names = ['get']

        
        
class LagnaPersonsOpinionViewSet(ModelViewSet):
    serializer_class = LagnaPersonOpinionSerializer
    pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated]
    queryset = LagnaPersonsOpinions.objects.all()
    http_method_names = ['get','post','delete','patch']

    def get_queryset(self):
        user = self.request.user
        condition = Q(active_flag=True,delete_flag=False)
        return LagnaPersonsOpinions.objects.filter(condition)

    @transaction.atomic
    def perform_create(self, serializer):
        try:
            serializer.save(create_user = self.request.user)
        except Exception as e:
            transaction.set_rollback(True)
            raise ValidationError(str(e))


    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active_flag=False
        instance.delete_flag=True
        instance.delete_user = self.request.user
        instance.delete_date = timezone.now()
        instance.save()
        return Response({'status':'ok'},status=status.HTTP_200_OK)



class LagnaTypeSpacificViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LagnaTypeSpacificSerializerBasic
    pagination_class = CustomPaginator
    http_method_names = ['get','post','patch']

    def get_queryset(self):
        user = self.request.user
        query = LagnaTypeSpacific.objects.none()
        if user.is_superuser:
            query = LagnaTypeSpacific.objects.all()
        
        else:
            # filter lagnatypespacific if user created or the main lagna created by user
            query = LagnaTypeSpacific.objects.filter(Q(create_user = user)| Q(committe_code__create_user = user))


        filter_keys = self.request.query_params
        model_fields = set(field.name for field in Lagna._meta.fields)
        # final_field = set(field for field in  filter_keys.keys() if field in model_keys  )
        condition = Q(delete_flag=False,active_flag=True)
        
        for field_name,field_value in filter_keys.items():
            if field_name in model_fields and field_value:
                field = Lagna._meta.get_field(field_name)
                if isinstance(field,models.CharField):
                    condition &=Q(**{f'{field_name}__icontains':field_value})
                elif isinstance(field,models.ForeignKey):
                    condition &=Q(**{f'{field_name}__id':field_value})
                elif isinstance(field,models.IntegerField):
                    condition &=Q(**{f'{field_name}__exact':field_value})

        return query.filter(condition)

    @transaction.atomic
    def perform_create(self, serializer):
        try:
            serializer.save(create_user = self.request.user)

        except Exception as e:
            transaction.set_rollback(True)
            raise ValidationError(str(e))


class LagnaOpinionsViewSet(ModelViewSet):
    # pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated]
    serializer_class = OpinionTypeSerializer
    queryset =  OpinionType.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        try:
            query = OpinionType.objects.filter(active_flag=True,delete_flag=False)
            person_id = self.request.query_params.get('person_id')
            disallowed_opinion = []
            if person_id:
                person_id = LagnaPersons.objects.get(pk=person_id)

                lagna = person_id.committe_type_code.committe_type
                if lagna.type_id == 1:
                    disallowed_opinion.extend([6,4,7])            # راي الافراد وراي رائيس هيئة تنظيم واداره 
                    # query.filter(~Q(pk__in = {6,4}))
                    lagna_prnt_army = person_id.committe_type_code.committe_code.prnt_army_code_id
                    child_army = set(ArmyParentChild.objects.filter(parent_code=lagna_prnt_army).values_list('child_code',flat=True))
                    if person_id.mil_ser.prnt_army_code == lagna_prnt_army:
                        # query.filter(~Q(pk__in = {3}))
                        disallowed_opinion.extend([3])          # راي السلاح
                    elif person_id.mil_ser.army_code in child_army:
                        # query.filter(~Q(pk__in = {3}))
                        if person_id.mil_ser.prnt_army_code == person_id.mil_ser.army_code:
                            disallowed_opinion.extend([2])          # راي التبعية
                        else:
                            disallowed_opinion.extend([2,1])          # راي التبعية



            condition = ~Q(pk__in=disallowed_opinion)
            

            # print(condition)
            if self.request.user.is_superuser or self.request.user.has_perm('lagna.can_see_all_opinion_type'):
                return query
            return query.filter(condition)
        except Exception as e:
            raise ValidationError(str(e))

    def list(self, request, *args, **kwargs):

        data ={} 
        queryset = self.get_queryset()
        data['opinions'] = self.get_serializer(queryset,many=True).data

        votes = LagnaVoteOpinoin.objects.all()
        person_id = self.request.query_params.get('person_id')
        person_id = LagnaPersons.objects.get(pk=person_id)
        if person_id:
            # print(person_id.committe_type_code.committe_type_id)
            votes = LagnaVoteOpinoin.objects.filter(committe_type_code_id = person_id.committe_type_code.committe_type_id)
        serializer = LagnaVoteOpinoinSerializer(votes,many=True)
        data['votes'] = serializer.data

        return Response(data)


class BenefitTypeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BenefitTypeSerializer
    queryset = BenefitType.objects.all()
    http_method_names = ['get']

        

class CommanderJobTypeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommanderJobTypeSerializer
    queryset = CommanderJobType.objects.all()
    http_method_names = ['get']
