
from rest_framework.renderers import BaseRenderer
from django.db.models import Q, Prefetch,F,Value,Sum,Count
from django.http import StreamingHttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed,ValidationError
from django.utils import timezone
from django.db import transaction,models
from django.db.models import Q,OuterRef,Exists
from django.contrib.auth.models import User,Group
from apps.users.serializers import UserSerializerBasic,CreateUserSerializer
from apps.lagna.models import LagnaMemberType
from apps.lagna.serializers import LagnaMemberTypeSerializer,LagnaReportSerilaizer
from apps.person.serializers import AfrPersonSerializerBasic,AfrPersonSerializerDetails
from apps.tanzem.models import ArmyParentChild
from apps.person.models import AfrPerson
from apps.report.models import LagnaAfrReport
from apps.report.serializers import LagnaAfrReportSerializer
from apps.report.services.generate_lagna_report import generate_lagna_report
from utilts.filters import get_filter_cond
from .services.get_or_create_snap import get_or_create_snap
from datetime import datetime,timedelta
from .utilts import send_websocket_data
import json
from django.core.cache import cache
from .permissions import AllowToVote
from .serializers import (
    OpinionTypeSerializer,
    LagnaPersonSerializerDetails,
    LagnaPersonSerializerBasic,
    LagnaPersonWithSnapSerializerBasic,
    LagnaPersonOpinionSerializer,
    # LagnaTypeSpacificSerializerBasic,
    LagnaTypeSpacificSerializerInfo,
    LagnaTypeSpacificSerializerDetails,
    LagnaVoteOpinoinSerializer,
    LagnaMemberSerializer,
    LagnaPeronVotesSerializer,
    LagnaPersonPhotoReportSerializer,
    LagnaStatusSerializer,
    LagnaPersonReasonsSerializer,
    LagnaAfrSnapDataSerializer,
    LagnaGetCommSnapSerializer,
    AfrSnapFinalDecitionSerializer,
    AfrSnapOpinionSerializer,
    AfrSnapCustomReportInfoSerializer,
    LagnaReportSerilaizer,
    LagnaPersonReportSerializer,
    LagnaSpacificReportSerializer,
    LagnaSpacificOpinionsReportSerializer,
    
    )
from .models import (
    OpinionType,
    LagnaPersonsOpinions,
    Lagna,
    LagnaPersonVotes,
    LagnaPersons,
    LagnaTypeSpacific,
    LagnaAfrStatus,
    LagnaVoteOpinoin,
    LagnaAfrSnapData,
    LagnaCommanderData,
    AfrSnapFinalDecition,
)
from .permissions import (
    AllowToAddOrEditPerson,
    AllowToSetReview,
    AllowToSetConf,
    AllowToSetWaitingDate,
    AllowToSetOpinion,
    )


class LagnaSpacificMixin:
    @transaction.atomic
    @action(detail=True,methods=['get','patch'],url_path='lagna-spacific(?:/(?P<spacific_id>\d+))?')
    def get_lagna_spacific(self,request,pk=None,spacific_id=None):
        try:
            lagna = self.get_object()
            lagna_type_spacific = lagna.lagna_type_spacific.filter(active_flag=True,delete_flag=False)
            if self.request.method == 'GET':
                if spacific_id:
                    query = lagna_type_spacific.get(pk=spacific_id)
                    serializer =LagnaTypeSpacificSerializerInfo(query)
                    return Response(serializer.data,status=status.HTTP_200_OK)
                page = self.paginate_queryset(lagna_type_spacific)
                paginator = self.paginator
                serializer =LagnaTypeSpacificSerializerInfo(page,many=True)
                return paginator.get_paginated_response(serializer.data)
            elif self.request.method == 'PATCH':
                if not spacific_id:
                    raise ValidationError('should send lagna spacific id in the request url')
                data = self.request.data.copy()
                lagna_spacific = lagna_type_spacific.get(pk=spacific_id)
                # print(lagna_spacific)
                serializer =LagnaTypeSpacificSerializerInfo(lagna_spacific,data=data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True,methods=['post'],url_path='lagna-spacific/add')
    def create_lagna_spacific(self,request,pk=None):
        try:
            instance = self.get_object()
            if self.request.method == 'POST':
                data = self.request.data.copy()
                data['committe_code'] = instance.pk
                serializer =LagnaTypeSpacificSerializerInfo(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(create_user = self.request.user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            elif self.request.method == 'GET':   
                query = LagnaTypeSpacific.objects.filter(committe_code=instance)
                serializer =LagnaTypeSpacificSerializerInfo(query,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    @transaction.atomic
    @action(detail=True,methods=['get'],url_path='lagna-spacific/(?P<spacific_id>\d+)/sort')
    def sort_lagna_spacific(self,request,pk=None,spacific_id=None):
        try:
            degree_eq = {
                1:1,
                2:2,
                3:3,
                4:4,
                5:5,
                6:6,
                7:7,
                8:8,
                9:9,
                10:10,
                11:11
            }
            lagna = self.get_object()
            lagna_type_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            persons = lagna_type_spacific.lagna_persons.filter(active_flag=True,delete_flag=False)
            persons = persons.annotate(degree_eq=degree_eq.get(F('degree_code'))).order_by('mil_ser__army_code','-mil_ser__person_sex_code','-degree_eq','mil_ser__mil_no')
            range_dates = [ waiting_date.date() for waiting_date in sorted(set(persons.values_list('person_committe_date',flat=True))) if waiting_date != None].append(None)
            main_counter = 1
            for date in range_dates:
                counter = 1
                persons_per_day = persons.filter(person_committe_date = date)
                for person in persons_per_day:
                    person.update(person_order_day=counter,committe_order=main_counter)

                    main_counter += 1
                    counter += 1

        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    @transaction.atomic
    @action(detail=True,methods=['get'],url_path='lagna-spacific/(?P<spacific_id>\d+)/clear-cache')
    def clear_cache_lagna_spacific(self,request,pk=None,spacific_id=None):
        try:
            cache.clear()
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['get'],url_path='lagna-spacific/(?P<spacific_id>\d+)/report')
    def get_lagna_spacific_statistics_report(self,request,pk=None,spacific_id=None):
        try:
            lagna = self.get_object()
            spacific = lagna.lagna_type_spacific.filter(pk=spacific_id,active_flag=True,delete_flag=False).first()
            serializer = LagnaSpacificReportSerializer(spacific)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['get'],url_path='lagna-spacific/(?P<spacific_id>\d+)/opinions-report')
    def get_lagna_spacific_opinions_report(self,request,pk=None,spacific_id=None):
        try:
            lagna = self.get_object()
            spacific = lagna.lagna_type_spacific.filter(pk=spacific_id,active_flag=True,delete_flag=False).first()
            serializer =LagnaSpacificOpinionsReportSerializer(spacific)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['get'],url_path='lagna-spacific/(?P<spacific_id>\d+)/photo-report')
    def get_lagna_spacific_photo_report(self,request,pk=None,spacific_id=None):
        try:
            lagna = self.get_object()
            spacific = lagna.lagna_type_spacific.filter(pk=spacific_id,active_flag=True,delete_flag=False).first()
            persons = spacific.lagna_persons.filter(active_flag=True,delete_flag=False).all()
            page = self.paginate_queryset(persons)
            serializer =LagnaPersonPhotoReportSerializer(page,many=True)
            paginator = self.paginator
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)



class LagnaSpacificMemberMixin:
    @transaction.atomic
    @action(detail=True, methods=['get'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/members(?:/(?P<member_id>\d+))?')
    def get_member(self,request,pk=None,spacific_id=None,member_id=None):
        try:
            lagna = self.get_object()
            # lagna_type_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            members =lagna.members.filter(active_flag=True,delete_flag=False)
            if member_id:
                member = members.get(pk=member_id)
                serializer = LagnaMemberSerializer(member)
                return Response(serializer.data,status=status.HTTP_200_OK)
            page = self.paginate_queryset(members)
            paginator = self.paginator
            serializer = LagnaMemberSerializer(page,many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['post'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/members/add')
    def add_member(self,request,pk=None,spacific_id=None):
        try:
            lagna = self.get_object()
            # lagna_type_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)

            data = self.request.data.copy()
            data['committe_code'] = lagna.pk
            serializer = LagnaMemberSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(create_user = self.request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['post'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/members/new')
    def add_new_member(self,request,pk=None,spacific_id=None):
        try:
            lagna = self.get_object()
            lagna_type_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            data = self.request.data.copy()
            serializer = CreateUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**serializer.validated_data)

            user.profile.password = data.get('password',None)
            user.profile.rank_name = data.get('rank_name',None)
            user.profile.job = data.get('job',None)
            user.profile.save()

        
            

            data['committe_code'] = lagna_type_spacific.pk
            data['member_user']  = user.pk
            serializer = LagnaMemberSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(create_user = self.request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['delete'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/members/(?P<member_id>\d+)/delete')
    def delete_member(self,request,pk=None,spacific_id=None,member_id=None):
        try:
            if not member_id:
                raise MethodNotAllowed(self.request.method)
            lagna = self.get_object()
            # lagna_type_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            members =lagna.members.filter(active_flag=True,delete_flag=False)
            member = members.get(pk=member_id)
            member.active_flag= False
            member.delete_flag = True
            member.delete_user = self.request.user
            member.delete_date = timezone.now()
            member.save()
            return Response(f'{member.member_user.username} {member.member_user.get_full_name()} deleted',status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'details':str(e)},status=status.HTTP_400_BAD_REQUEST)


class EventStreamRender(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'event-stream'
    charset ='utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class LagnaShowMixin:
    # @action(detail=True, methods=['get'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/ready')
    # def cache_lagna_person(self,request,pk=None,spacific_id=None):
    #     try:
    #         # print(self.request.data.get_list('mil_ser'))
    #         lagna = self.get_object()
    #         lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
    #         persons = (
    #             lagna_spacific.lagna_persons
    #             .filter(active_flag=True, delete_flag=False)
    #             .select_related("mil_ser")
    #         )

    #         mil_sers = [p.mil_ser for p in persons]

    #         serialized = AfrPersonSerializerDetails(mil_sers, many=True).data

    #         data = {}

    #         for person, ser_data in zip(persons, serialized):
    #             key = f"mil_ser_{person.mil_ser.mil_ser}"
    #             data[key] = ser_data

    #         cache.set_many(data, 3600)
    #         return Response(len(mil_sers))

    #     except Exception as e:
    #         return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    def event_stream(self,persons):
        total = persons.count()
        count = 0
        for person in persons.iterator(chunk_size=50):
            # serializer =LagnaPersonSerializerDetails(person)
            serializer =AfrPersonSerializerDetails(person.mil_ser)
            # key = f'lagna_{lagna.committe_code}_spacific_{lagna_spacific.committe_code}_person_{person.person_id}'
            key=f'mil_ser_{person.mil_ser.mil_ser}'
            # data[key] = serializer.data
            count += 1
            cache.set(key,serializer.data)
            # print(count)
            yield f"data: {count}/{total}\n\n"


    @action(detail=True, methods=['get'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/ready',renderer_classes = [EventStreamRender])
    def cache_lagna_person(self,request,pk=None,spacific_id=None):
        try:
            # print(self.request.data.get_list('mil_ser'))
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
            persons = lagna_spacific.lagna_persons.filter(active_flag=True,delete_flag=False)
            data = {}
            def generate():
                total = persons.count()
                count = 0
                for person in persons.iterator():
                    # serializer =LagnaPersonSerializerDetails(person)
                    serializer =AfrPersonSerializerDetails(person.mil_ser)
                    # key = f'lagna_{lagna.committe_code}_spacific_{lagna_spacific.committe_code}_person_{person.person_id}'
                    key=f'mil_ser_{person.mil_ser.mil_ser}'
                    # data[key] = serializer.data
                    count += 1
                    # print(count)
                    cache.set(key,serializer.data)
                    yield f"cached: {count}/{total}\n"
            # cache.set_many(data,3600)
            # response = StreamingHttpResponse(self.event_stream(persons[:10]),content_type = 'text/event-stream')
            response = StreamingHttpResponse(generate(),content_type = 'text/event-stream')
            response['Cache-Control'] = 'no-cache'
            response['X-Accel-Buffering'] = 'no'
            response['Transfer-Encoding'] = 'chunked'
            return response
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    @action(detail=True, methods=['get'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/show')
    def show_person(self,request,pk=None,spacific_id=None,person_id=None):
        # try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            #--------------------------------------------------------------------
            # 
            #--------------------------------------------------------------------
            # key = f'lagna_{lagna.committe_code}_spacific_{lagna_spacific.committe_code}_person_{person.person_id}'
            key = f'mil_ser_{person.mil_ser.mil_ser}'
            show_now_key = f'comm_{lagna.committe_code}_now'
            group_name =  f'comm_{lagna.committe_code}'
            main_data = cache.get(key)
            # print('cached ',main_data)
            comm_data = LagnaPersonWithSnapSerializerBasic(person).data
            if not main_data:
                main_data =AfrPersonSerializerDetails(person.mil_ser).data
            json_data =json.dumps( { 
                'main_data':main_data,
                'comm_data': comm_data,
                'event':'show_person',
                }
                )
            # print('*'*7,group_name)
            send_websocket_data(json_data,group_name,'show_person')
            cache.set(group_name,json_data)
            cache.set(key,main_data)
            cache.set(show_now_key,person.pk)
            return Response(person.mil_ser.person_name)
        # except Exception as e:
            # transaction.set_rollback(True)
            raise Exception(e)
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['post'],url_path='event')
    def controler(self,request,pk=None,spacific_id=None,person_id=None):
        try:
            lagna = self.get_object()
            comm_key = f'comm_{lagna.pk}'
            members_key = comm_key+'_voter'
            head_key = comm_key+'_head'

            operation = self.request.data.get('operation')
            lagna_spacific_id = self.request.data.get('spacific_code')
            person_id = self.request.data.get('person_id')
            # print('operation',operation)

            if not operation:
                raise ValidationError('should set operation param')

            # re show person with comm data
            if operation == 'reset':
                show_now_key = comm_key+'_now'
                person_id = cache.get(show_now_key)
                if person_id:
                    person = LagnaPersons.objects.filter(pk=person_id).first()
                    if person:
                        person.votes.update(active_flag=False,delete_flag=True)
                        key = f'mil_ser_{person.mil_ser.mil_ser}'
                        show_now_key = f'comm_{lagna.committe_code}_now'
                        group_name =  f'comm_{lagna.committe_code}'
                        main_data = cache.get(key)
                        # print('cached ',main_data)
                        comm_data = LagnaPersonWithSnapSerializerBasic(person).data
                        if not main_data:
                            main_data =AfrPersonSerializerDetails(person.mil_ser).data
                        json_data =json.dumps( { 
                            'main_data':main_data,
                            'comm_data': comm_data,
                            'event':'show_person',
                            }
                            )
                        # print('*'*7,group_name)
                        send_websocket_data(json_data,group_name,'show_person')
                        send_websocket_data('start_voting',members_key,'notify')
                        send_websocket_data('voting',head_key,'notify')
                return Response({'event':operation,'person':person.mil_ser.person_name})
            if operation == 'start_voting':
                members_key = comm_key+'_voter'
                head_key = comm_key+'_head'
                send_websocket_data(operation,members_key,'notify')
                send_websocket_data('voting',head_key,'notify')
                return Response({'operation':operation,'lagna':lagna.pk,'key':members_key})

            if operation == 'clear_cache':
                try:
                    cache.delete(comm_key)
                    # cache.clear()
                except Exception as e:
                    return Response({'error':str(e)})
            if operation == 'opinions_report':
                spacific = lagna.lagna_type_spacific.filter(pk=lagna_spacific_id).first()
                data = LagnaSpacificOpinionsReportSerializer(spacific).data
                payload = json.dumps({
                    'data':data,
                    'event':operation
                })
                send_websocket_data(payload,comm_key,'show_person')
                return Response({'operation':operation,'lagna':lagna.pk})
            if operation.startswith('comm_report'):
                # data = LagnaReportSerilaizer(lagna,context={'type_code':self.request.data.get('spacific_code')}).data
                spacific = lagna.lagna_type_spacific.filter(pk=lagna_spacific_id).first()
                data = LagnaSpacificReportSerializer(spacific).data

                payload = json.dumps({
                    'data':data,
                    'event':operation
                })
                send_websocket_data(payload,comm_key,'show_person')
                return Response({'operation':operation,'lagna':lagna.pk})
            send_websocket_data(operation,comm_key,'notify')
            return Response({'operation':operation,'lagna':lagna.pk})
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
            
class LagnaReportMixin:
    @action(detail=True,methods=['get'],url_path='report')
    def get_lagna_report(self,request,pk=None):
        try:
            lagna = self.get_object()
            serializer = LagnaReportSerilaizer(lagna)

            return Response(serializer.data)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['get',],url_path='lagna-spacific/(?P<spacific_id>\d+)/person-report')
    def get_lagna_spacific_report(self,request,pk=None,spacific_id=None):
        try:
            lagna = self.get_object()
            spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            persons = spacific.lagna_persons.filter(active_flag=True,delete_flag=False)
            params = self.request.query_params
            persons = get_filter_cond(LagnaPersons,params,persons)
            # print(persons.values())
            page = self.paginate_queryset(persons)
            serializer =LagnaPersonReportSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)






class LagnaSpacificPersonMixin:
    @transaction.atomic
    @action(detail=True, methods=['get'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons(?:/(?P<person_id>\d+))?')
    def get_person(self, request, pk=None, spacific_id=None, person_id=None):
        try:
            lagna = self.get_object()

            # ---------------------------------
            # Prefetch and select_related for performance
            # ---------------------------------
            lagna_spacific = (
                lagna.lagna_type_spacific
                .filter(pk=spacific_id, active_flag=True, delete_flag=False)
                .select_related('committe_type')
                .prefetch_related(
                    Prefetch(
                        'lagna_persons',
                    )
                )
            ).first()

            if not lagna_spacific:
                return Response([], status=status.HTTP_400_BAD_REQUEST)

            persons = lagna_spacific.lagna_persons.filter(active_flag=True,delete_flag=False)

            user_army_code = request.user.profile.prnt_army_code_id

            # ---------------------------------
            # Restrict by army code efficiently
            # ---------------------------------
            # if not request.user.is_superuser and lagna.prnt_army_code_id != user_army_code:
            #     parent = ArmyParentChild.objects.filter(child_code=user_army_code).first()
            #     if parent and lagna.prnt_army_code_id == parent.parent_code:
            #         persons = persons.filter(
            #             Q(mil_ser__prnt_army_code=user_army_code) |
            #             Q(mil_ser__army_code=user_army_code)
            #         )

            # ---------------------------------
            # Filter by person_id if given
            # ---------------------------------
            if person_id:
                person = persons.get(pk=person_id)
                # print('get persons ',persons.count())
                serializer = LagnaPersonSerializerDetails(person)
                # print('get  after',persons.count())
                return Response(serializer.data)

            # ---------------------------------
            # Dynamic filtering
            # ---------------------------------
            filter_keys = request.query_params
            condition = Q()
            model_fields = [field.name for field in LagnaPersons._meta.fields]

            for field_name, field_value in filter_keys.items():
                if not field_value:
                    continue
                if field_name in model_fields:
                    field = LagnaPersons._meta.get_field(field_name)
                    if isinstance(field, models.CharField):
                        condition &= Q(**{f"{field_name}__icontains": field_value})
                    elif isinstance(field, models.IntegerField):
                        condition &= Q(**{f"{field_name}": field_value})
                    elif isinstance(field, models.ForeignKey):
                        condition &= Q(**{f"{field_name}_id": field_value})
                    elif isinstance(field,models.DateTimeField):
                        condition &= Q(**{f"{field_name}__date": field_value})

                else:
                    parts = field_name.split('__')
                    # print(field_name)
                    if len(parts) == 2:
                        child_field_name = parts[0]
                        rel_fd_name = parts[1]
                        if child_field_name in model_fields:
                            # print(rel_field_name)
                            rel_field = LagnaPersons._meta.get_field(child_field_name)
                            # print(rel_field)
                            # print(type(rel_field))
                            # print(rel_field.related_model)
                            related_model_fields = [field.name for field in rel_field.related_model._meta.fields]
                            if isinstance(rel_field,models.ForeignKey) and rel_fd_name in related_model_fields:
                                rel_fd_name_type = rel_field.related_model._meta.get_field(rel_fd_name)
                                if isinstance(rel_fd_name_type,models.CharField):
                                    condition &=Q(**{f'{field_name}__icontains':field_value})
                                elif isinstance(rel_fd_name_type,models.IntegerField):
                                    condition &=Q(**{f'{field_name}__exact':field_value})

            persons = persons.filter(condition)

            # ---------------------------------
            # Pagination
            # ---------------------------------
            page = self.paginate_queryset(persons)
            serializer = LagnaPersonSerializerBasic(page, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({'details': str(e)}, status=400)


    @transaction.atomic
    @action(detail=True, methods=['post'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/add')
    def add_person(self,request,pk=None,spacific_id=None):
            try:
                lagna = self.get_object()
                lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
                data = self.request.data.copy()
                data['committe_type_code'] = lagna_spacific.pk
                # print('before serializer :')
                serializer = LagnaPersonSerializerDetails(data=data)
                # print('after ')
                serializer.is_valid(raise_exception=True)
                person = serializer.validated_data.get('mil_ser')
                if lagna.committe_category_id == 1  and lagna.prnt_army_code_id != '0202' :
                    parent_army_code = lagna.prnt_army_code_id
                    child_codes = set(ArmyParentChild.objects.filter(parent_code = parent_army_code).values_list('child_code',flat=True))
                    if person.prnt_army_code not in child_codes:
                        raise ValidationError({'details':f'can not add this person who prnt-army {person.prnt_army_name}'})
                serializer.save(add_user= self.request.user)

                return Response(serializer.data)
            except Exception as e:
                transaction.set_rollback(True)
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['delete'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/delete')
    def delete_person(self,request,pk=None,spacific_id=None,person_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
            # print('**'*5,lagna_spacific)
            if not person_id:
                raise MethodNotAllowed(self.request.method)
            persons = lagna_spacific.lagna_persons.filter(active_flag=True,delete_flag=False)
            # print(persons.count())
            person = persons.get(pk=person_id)
            #------------------------------------------
            # لو الشخص
            #------------------------------------------
            
            main_lagna = lagna.main_committe_code
            if main_lagna:
                main_lagna_spacific = main_lagna.lagna_type_spacific.get(committe_type_id=lagna_spacific.committe_type.type_id,active_flag=True,delete_flag=False)
                main_lagna_spacific_person = main_lagna_spacific.lagna_persons.filter(mil_ser_id=person.mil_ser_id,active_flag=True,delete_flag=False).first()
            # if main_lagna_spacific_person:
            #     raise ValidationError('لا يمكن حذف هذا الفرد ترشيح هيئة تنظيم واداره')

            # get snap to delete
            snap = get_or_create_snap(person,request=self.request)

            # delete opinions of snap
            snap.opinions.update(active_flag=False,delete_flag=True,delete_user=self.request.user,delete_date=timezone.now())

            # delete reasons
            snap.reasons.update(active_flag=False,delete_flag=True,delete_user=self.request.user,delete_date=timezone.now())

            #delete snap
            snap.active_flag=False
            snap.delete_flag = False
            snap.delete_user = self.request.user
            snap.delete_date = timezone.now()
            snap.save()

            # delete person
            person.active_flag=False
            person.delete_flag=True
            person.delete_user = self.request.user
            person.delete_date = timezone.now()
            person.save()
            return Response({'message':f'{person.mil_ser.person_name} deleted'},status=status.HTTP_200_OK)


        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['get'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/opinions(?:/(?P<opinion_id>\d+))?')
    def get_opinions(self,request,pk=None,spacific_id=None,person_id=None,opinion_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
            person = lagna_spacific.lagna_persons.get(pk=person_id)
            snap_instance = get_or_create_snap(person,self.request)
            # opinions = person.lagna_opinions.filter(active_flag=True,delete_flag=False)
            opinions = snap_instance.opinions.all()
            if opinion_id:
                opinion = opinions.get(pk=opinion_id)
                # serializer = LagnaPersonOpinionSerializer(opinion)
                serializer = AfrSnapOpinionSerializer(opinion)
                return Response(serializer.data,status=status.HTTP_200_OK)
                
            page = self.paginate_queryset(opinions)
            paginator = self.paginator
            # serializer = LagnaPersonOpinionSerializer(opinions,many=True)
            serializer =AfrSnapOpinionSerializer(opinions,many=True)
            return paginator.get_paginated_response(serializer.data)


        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['post'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/opinions/add')
    def add_opinion(self,request,pk=None,spacific_id=None,person_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
            person = lagna_spacific.lagna_persons.get(pk=person_id)
            data = self.request.data.copy()
            # data['person_id'] = person.pk
            # serializer = LagnaPersonOpinionSerializer(data=data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save(create_user = self.request.user)
            # # add opinion to opinons table attached to snap
            snap_instance = get_or_create_snap(person,self.request)
            data['snap_id'] = snap_instance.pk
            snap_opinion_serializer = AfrSnapOpinionSerializer(data=data)
            snap_opinion_serializer.is_valid(raise_exception=True)
            snap_opinion_serializer.save(create_user=self.request.user)
            # sync opinion with final decition related to snap

            if snap_opinion_serializer.validated_data.get('opinion_type').pk != 1:
                payload = {
                    'snap_id_id':snap_instance.pk,
                    'committe_id_id':lagna.pk,
                    'comm_prnt_code_id':lagna.prnt_army_code_id,
                    'comm_type_id_id': lagna_spacific.committe_type_id,
                    'active_flag':True
                }
                fin_dec_instace,_=AfrSnapFinalDecition.objects.update_or_create(
                    **payload,
                    defaults={
                    'fin_dec':snap_opinion_serializer.validated_data.get('opinion_code',None),
                    'create_user' : self.request.user
                    }
                )

            #-----------------------------------------
            # update attach of the snap
            opinion_attach = snap_opinion_serializer.validated_data.get('opinion_attached')
            if opinion_attach:
                snap_instance.attach=opinion_attach
                snap_instance.save(update_fields=['attach'])
            return Response(snap_opinion_serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['delete'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/opinions/(?P<opinion_id>\d+)/delete')
    def delete_opinion(self,request,pk=None,spacific_id=None,person_id=None,opinion_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            # if person.committe_status_code_id in [ 20,30,40,50,60 ]:
                # raise Exception({"error":f'لا يمكن حذف هذا الرأي حاله الفرد {person.committe_status_code.afr_comm_status_name}'})
            if not opinion_id:
                return MethodNotAllowed(self.request.method)
            snap_instace = get_or_create_snap(person,self.request)
            # opinions = person.lagna_opinions.filter(active_flag=True,delete_flag=False)
            opinions = snap_instace.opinions.all()
            opinion = opinions.get(pk=opinion_id)
            opinion.active_flag= False
            opinion.delete_flag = True
            opinion.delete_user = self.request.user
            opinion.delete_date = timezone.now()
            opinion.save()

            return Response(f'{person.mil_ser.person_name} {person.committe_type_code.committe_type.type_name} deleted',status=status.HTTP_200_OK)

        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['get'],permission_classes=[AllowToVote], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/votes(?:/(?P<vote_id>\d+))?')
    def get_vote(self,request,pk=None,spacific_id=None,person_id=None,vote_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            votes = person.votes.filter(active_flag=True,delete_flag=False)
            if vote_id:
                vote = votes.get(pk=vote_id)
                serializer = LagnaVoteOpinoinSerializer(vote)
                return Response(serializer.data,status=status.HTTP_200_OK)
            
            page = self.paginate_queryset(votes)
            paginator = self.paginator
            serializer = LagnaPeronVotesSerializer(page,many=True)
            return paginator.get_paginated_response(serializer.data)
            
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/votes/add')
    def add_vote(self,request,pk=None,spacific_id=None,person_id=None,vote_id=None):
        try:
            user = self.request.user                                                                            # get login user
            lagna = self.get_object()                                                                           # get main lagna

            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)   # get lagna spacifc like عدم صلاحية و استقاله الخ
            lagna_members =lagna.members.filter(active_flag=True,delete_flag=False)          # get lagna spacifc member  
            condition = Q(Q(member_user_id = user.pk)&~Q(member_type_id = 0))                                   # make condition to get user and can vote 
            member = lagna_members.get(condition)                                                      # make user the uesr is lagna member and can vote 
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)          # get the user is be voted
            # if person.committe_status_code_id < 40:                                                             # can not set vote before it status < 40    40 = منتظر انعقاد اللجنة
                # return Response({'details':f' لا يمكن وضع قرار نهائي لهذا الفرد حاله الفرد {person.committe_status_code.afr_comm_status_name}'},status=status.HTTP_400_BAD_REQUEST)
            data = self.request.data.copy()                                                                     # get required data ( vote )
            #-------------------------------------------------
            # set person and member automatically
            #-------------------------------------------------
            data ['person_id'] = person.pk                                                                      # set  person in lagna
            data ['vote_member_id'] = member.pk                                                                 # set lagna member 
            
            serializer =LagnaPeronVotesSerializer(data=data)                                                    # send data to serializer
            person.votes.filter(vote_member_id =member,active_flag=True).update(        
                active_flag=False,
                delete_flag=True,
                delete_date=timezone.now(),
                )                                                                                               # set vote belong to this member to be un active 

            serializer.is_valid(raise_exception=True)                                                           # make sure the data is valid
            if serializer.validated_data.get('vote_member_id').member_type_id == 1:

                #--------------------------------------------------------------------
                # set final decisioin equal راي رئيس اللجنة  till add final decision
                #--------------------------------------------------------------------
                person.committe_decision = serializer.validated_data.get('vote')
                person.committe_decision_date = timezone.now()
                person.save(update_fields = ['committe_decision','committe_decision_date'])
                print('i am herer :',serializer.validated_data.get('vote'))

                #---------------------- add final dection in snap final dection -------------------------------------------------------
                # 
                #-----------------------------------------------------------------------------

                snap_filter = {
                    'mil_ser' : person.mil_ser_id,
                    'root_committe': person.committe_type_code.committe_code.main_committe_code,
                    'committe_type': person.committe_type_code.committe_type
                }
                print('%'*20)

                afr_data = person.mil_ser
                comm_type_id = person.committe_type_code.committe_type_id
                current_lagna = person.committe_type_code.committe_code
                root_comm_id = current_lagna.main_committe_code_id or current_lagna.pk

                snap_instance = get_or_create_snap(person,self.request)
                # snap_instance, _ = LagnaAfrSnapData.objects.get_or_create(
                #     mil_ser_id=afr_data.mil_ser,
                #     committe_type_id=comm_type_id,
                #     root_committe_id=root_comm_id,
                #     active_flag=True,
                #     defaults={
                #         'unit_name': afr_data.unit_name, # Automated
                #         'unit_code': afr_data.unit_code, # Automated
                #         'army_code_id': afr_data.army_code, # Automated
                #         'prnt_army_code_id': afr_data.prnt_army_code,
                #         'degree_code': afr_data.degree_code,
                #         'to_unit_date': afr_data.to_unit_date ,
                #         'create_user': user
                #     }
                # )
                # committe_id = lagna.main_committe_code_id
                # if lagna.committe_category_id == 2:
                #     committe_id = lagna.pk
                # snap_instance.final_decition.update_or_create()
                payload = {
                    'snap_id_id':snap_instance.pk,
                    'committe_id_id':lagna.pk,
                    'comm_prnt_code_id':lagna.prnt_army_code_id,
                    'comm_type_id_id': lagna_spacific.committe_type_id,
                    'active_flag':True
                }
                fin_dec_instace,_=AfrSnapFinalDecition.objects.update_or_create(
                    **payload,
                    defaults={
                    'fin_dec_id':data.get('vote',None),
                    'create_user' : user
                    }
                )
                # serializer.is_valid(raise_exception=True)
                # serializer.save(create_user=self.request.user)



            
            # create new vote 
            serializer.save()                                                                                                   # save vote
            comm_data = LagnaPersonWithSnapSerializerBasic(person).data
            json_data = json.dumps({
                'comm_data': comm_data,
                'event':'vote'
                }
            )
            # if user i 
            member_type =None if member.member_type_id == 1 else 'head'
            if member_type:
                group_name = f'comm_{lagna.committe_code}_{member_type}'
            else:
                group_name = f'comm_{lagna.committe_code}'
            # print(f'send data to websocket {group_name}  ')
            # send_websocket_data(json_data,group_name,'send_votes')
            for_all = f'comm_{lagna.committe_code}'
            send_websocket_data(json_data,for_all,'send_votes')
            main_data = cache.get(f'mil_ser_{person.mil_ser_id}')
            print('^'*20)
            if main_data:
                lagna_cache_data = json.dumps({
                    'main_data':main_data,
                    'comm_data': comm_data,
                    'event':'show_person',
                })
                lagna_key = f'comm_{lagna.committe_code}'
                cache.set(lagna_key,lagna_cache_data)
            # print('done')
            
            return Response(serializer.data,status=status.HTTP_200_OK)
            
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['get'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/decision')
    def get_final_decision (self,request,pk=None,spacific_id=None,person_id=None,vote_id=None):
        try:
            lagna = self.get_object()                                                                           # get main lagna
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)   # get lagna spacifc like عدم صلاحية و استقاله الخ
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)          # get the user is be voted
            serializer =LagnaVoteOpinoinSerializer(person.committe_decision)
            data = serializer.data.copy()
            data['note'] = person.committe_decision_note
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'details':str(e)},status=status.HTTP_400_BAD_REQUEST)
    @transaction.atomic
    @action(detail=True, methods=['post'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/decision/add')
    def set_final_decision (self,request,pk=None,spacific_id=None,person_id=None,vote_id=None):
        try:
            user = self.request.user
            lagna = self.get_object()                                                                           # get main lagna
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)   # get lagna spacifc like عدم صلاحية و استقاله الخ
            lagna_spacific_members = lagna_spacific.members.filter(active_flag=True,delete_flag=False)          # get lagna spacifc member  
            condition = Q(Q(member_user_id = user.pk) & Q(member_type_id = 1))                                   # make condition to get user and can vote 
            try:
                member = lagna_spacific_members.get(condition)                                                      # make user the uesr is lagna member and can vote 
            except Exception as e:
                raise Exception('انت لست عضو في اللجنة او ليس لديك الصلاحية لوضع القرار النهائي')


            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)          # get the user is be voted

            decision = self.request.data.get('decision')
            decision_note = self.request.data.get('notes')
            if not decision:
                raise ValidationError('decision variable should be set')
            decision =LagnaVoteOpinoin.objects.get(pk=int(decision))
            person.committe_decision = decision
            person.committe_decision_note = decision_note
            person.committe_decision_date = timezone.now()
            person.save()
            serializer = LagnaVoteOpinoinSerializer(person.committe_decision)
            data = serializer.data.copy()
            data['note'] = person.committe_decision_note if person.committe_decision_note else ""


            #--------------------------------------
            # send data to lagna member
            #--------------------------------------
            json_data = json.dumps(
                LagnaPersonWithSnapSerializerBasic(person).data
            )
            # if user i 
            member_type =None if member.member_type_id == 1 else 'head'
            if member_type:
                group_name = f'comm_{lagna.committe_code}_{member_type}'
            else:
                group_name = f'comm_{lagna.committe_code}'
            # print(f'send data to web socker {group_name}  ')
            send_websocket_data(json_data,group_name,'send_votes')
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'details':str(e)},status=status.HTTP_400_BAD_REQUEST)


class LagnaPersonReasonsMixin:
    @transaction.atomic
    @action(detail=True, methods=['get','patch'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/reasons(?:/(?P<reason_id>\d+))?')
    def get_reasons(self,request,pk=None,spacific_id=None,person_id=None,reason_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            # print('ok'*7)
            # print('person_id',person_id)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            person_snap = get_or_create_snap(person,self.request)
            reasons = person_snap.reasons.filter(active_flag=True,delete_flag=False)
            if self.request.method == 'GET':
                if reason_id:
                    reason = reasons.get(pk=reason_id)
                    serializer = LagnaPersonReasonsSerializer(reason)
                    return Response(serializer.data,status=status.HTTP_200_OK)
                serializer = LagnaPersonReasonsSerializer(reasons,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            elif self.request.method == 'PATCH':
                if not reason_id:
                    raise MethodNotAllowed('should send reason id in the url')
                reason = reasons.get(reason_id)
                data = self.request.data.copy()
                serializer = LagnaPersonReasonsSerializer(reason,data=data)
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['post'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/reasons/add')
    def add_reasons(self,request,pk=None,spacific_id=None,person_id=None,reason_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            data = self.request.data.copy()
            person_snap = get_or_create_snap(person,self.request)
            data['snap_id'] = person_snap.pk
            serializer = LagnaPersonReasonsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(create_user=self.request.user)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['delete'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/reasons/(?P<reason_id>\d+)/delete')
    def delete_reasons(self,request,pk=None,spacific_id=None,person_id=None,reason_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            snap_id = get_or_create_snap(person)
            reason = snap_id.reasons.get(pk=reason_id,active_flag=True,delete_flag=False)
            reason.active_flag = False
            reason.delete_flag = True
            reason.delete_user_id = self.request.user.pk
            reason.delete_date = timezone.now()
            reason.save()
            return Response({'ok':'deleted'},status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=True, methods=['get','patch'],permission_classes=[AllowToAddOrEditPerson], url_path=r'lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/add-reason')
    def person_add_reason(self,request,pk=None,spacific_id=None,person_id=None):
        """سبب العرض - the single free text stored on the snap itself"""
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            person_snap = get_or_create_snap(person,self.request)

            if self.request.method == 'PATCH':
                add_reason = self.request.data.get('add_reason')
                if add_reason is not None and len(add_reason) > 2000:
                    raise ValidationError('سبب العرض لا يمكن ان يزيد عن 2000 حرف')
                person_snap.add_reason = add_reason or None
                person_snap.save(update_fields=['add_reason'])

            return Response(
                {'snap_id':person_snap.pk,'add_reason':person_snap.add_reason},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            transaction.set_rollback(True)
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)


class SnapDataMixin:
    @transaction.atomic
    @action(detail=True, methods=['get','post'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/snap')
    def get_snap_data(self,request,pk=None,spacific_id=None,person_id=None,snap_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id,active_flag=True,delete_flag=False)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            if self.request.method == 'GET':
                 # 1. Get the current person context
                # 2. Identify the anchors
                afr_data = person.mil_ser
                mil_ser_id = person.mil_ser_id
                comm_type_id = person.committe_type_code.committe_type_id
                current_lagna = person.committe_type_code.committe_code
                root_comm_id = current_lagna.main_committe_code_id or current_lagna.pk

                # 3. Find the shared Snap
                # snap = LagnaAfrSnapData.objects.prefetch_related(
                #     # 'commanders', 
                #     # 'commanders__person_cons_pons',
                #     # 'commanders__opinions__person_id__committe_type_code__committe_code'
                # ).get(
                #     mil_ser_id=mil_ser_id,
                #     committe_type_id=comm_type_id,
                #     root_committe_id=root_comm_id,
                #     active_flag=True
                # )
                snap = get_or_create_snap(person,self.request)
                # snap , _ = LagnaAfrSnapData.objects.get_or_create(
                #     mil_ser_id=mil_ser_id,
                #     committe_type_id=comm_type_id,
                #     root_committe_id=root_comm_id,
                #     active_flag=True,
                #     defaults={
                #         'unit_name': afr_data.unit_name, # Automated
                #         'unit_code': afr_data.unit_code, # Automated
                #         'army_code_id': afr_data.army_code, # Automated
                #         'prnt_army_code_id': afr_data.prnt_army_code,
                #         'degree_code_id': afr_data.degree_code,
                #         'to_unit_date': afr_data.to_unit_date ,
                #         'create_user': self.request.user
                #     }
                # )

                comm_snap_data = snap.comm_snap_detail.filter(active_flag=True,delete_flag=False)
                # serializer = LagnaAfrSnapDataSerializer(snap)

                # serializer = LagnaGetCommSnapSerializer(comm_snap_data,many=True)
                serializer =AfrSnapCustomReportInfoSerializer(snap)

                return Response(serializer.data)
            if self.request.method == 'POST':
                data = self.request.data.copy()
                data['person_id'] = person.pk
                serializer = LagnaAfrSnapDataSerializer(data=data,context ={'request':self.request})
                serializer.is_valid(raise_exception=True)
                snap_instance = serializer.save()
                comm_snap_data = snap_instance.comm_snap_detail.filter(active_flag=True,delete_flag=False)
                # get_serializer = LagnaGetCommSnapSerializer(comm_snap_data,many=True)
                serializer = AfrSnapCustomReportInfoSerializer(snap_instance)

                return Response(serializer.data)

        except LagnaPersons.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"error": "Person record not found"}, status=status.HTTP_404_NOT_FOUND)
        except LagnaAfrSnapData.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"error": "No snapshot found for this person journey"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.set_rollback(True)
            raise ValidationError(str(e))



class LagnaPersonStatusMixin:
    @transaction.atomic
    @action(detail=True, methods=['post'],permission_classes=[AllowToAddOrEditPerson], url_path='lagna-spacific/(?P<spacific_id>\d+)/persons/(?P<person_id>\d+)/status')
    def set_status(self,request,pk=None,spacific_id=None,person_id=None):
        try:
            lagna = self.get_object()
            lagna_spacific = lagna.lagna_type_spacific.get(pk=spacific_id)
            person = lagna_spacific.lagna_persons.get(pk=person_id,active_flag=True,delete_flag=False)
            snap_instance = get_or_create_snap(person,self.request)

            # opinions = person.lagna_opinions.filter(active_flag=True,delete_flag=False)
            opinions = snap_instance.opinions.all()
            new_status = self.request.data.get('new_status')
            if not new_status:
                raise ValidationError('new_status variable should be set')
            new_status = LagnaAfrStatus.objects.get(pk=new_status).afr_comm_status_code                 # check if the status exists




            if new_status == 20:
                person.review_user_id = self.request.user.pk
                person.review_date = timezone.now()
            elif new_status == 30:
                person.conf_user_id = self.request.user.pk
                person.conf_date = timezone.now()
            elif new_status == 40:                              # منتظر انعقاد اللجنة
                if lagna_spacific.start_date == lagna_spacific.end_date :
                    person.person_committe_date = lagna_spacific.end_date
                else:
                    # should set waiting_date in post data
                    waiting_date = request.data.get('waiting_date')
                    if not waiting_date:
                        raise ValidationError('waiting_date not set')
                #------------------------------------------------------------
                # the waiting date should be in range start <= waiting >= end
                #------------------------------------------------------------
                    start_date = lagna_spacific.start_date.date()
                    end_date=lagna_spacific.end_date.date()
                    waiting_date=timezone.make_aware(datetime.strptime(waiting_date,'%Y-%m-%d'))
                    range_date = [
                        (start_date + timedelta(days=i))
                        for i in range((end_date-start_date).days + 1)
                    ]
                    if waiting_date.date() not in range_date:
                        raise ValidationError({'error':f'the waiting date should be in range {range_date}'})


                # set status to be waiting to lagna
                person.committe_user_date_id = self.request.user.pk
            elif new_status == [50,60]:
                person.attend_user_id = self.request.user.pk
                person.attend_user_date = timezone.now()

            person.committe_status_code_id = new_status
            person.save()
            serializer = LagnaStatusSerializer(person.committe_status_code)
            return Response(serializer.data)



            return Response(serializer.data)
            if new_status == 20:            # new status is مراجع
                if person.committe_status_code_id == 10:                                # حاله الفرد مسجل
                    #--------------------------------------------------------------------------------
                    # if prnt_army_code == army_code  and  prnt_army_code  same in lagna and person
                    #                                                   -> unit_opinoin
                    #                                                   -> army_code
                    # if prnt_army_code != army_code        
                    #                   if prnt_army_code == lagna.prnt_army_code
                    #                                                   -> unit_opinon
                    #                                                   -> prnt_army_code
                    #                   if army_code == lagna.prnt_army_code
                    #                                                   -> unit_opinon
                    #                                                   -> prnt_army_code opinion
                    #                                                   -> army_code opinon
                    #--------------------------------------------------------------------------------
                    # try:
                    #     unit_opinion = opinions.get(opinion_type_id =1,active_flag=True,delete_flag=False)        # if return so it is exists
                    # except Exception as e:
                    #     raise Exception('يجب وضع رأي الوحدة')

                    # if person.mil_ser.prnt_army_code == person.mil_ser.army_code:
                    #     try:
                    #         army_opinion = opinions.filter(opinion_type_id__in = [ 2,3],active_flag=True,delete_flag = False)
                    #     except Exception as e:
                    #         raise Exception('يجب وضع راي السلاح')

                    # else:
                    #     try:
                    #         #-------------------------------------------------------------------
                    #         # راي التبعية يجب ان يكون من لجنة فرعية 
                    #         # like person.lagna_spacific.lagna.main_committe_code.child_parnt.get
                    #         #-------------------------------------------------------------------
                    #         prnt_army_opinion = opinions.get(opinion_type_id = 2,active_flag=True,delete_flag=False)
                    #     except Exception as e:
                    #         raise Exception('يجب وضع راي التشكيل')


                    #--------------------------------------------------------
                    # set new status and set the review user and date
                    #--------------------------------------------------------
                    person.committe_status_code_id = new_status
                    person.review_user_id = self.request.user.pk
                    person.review_date = timezone.now()
                    person.save()

            elif new_status == 30:          # new status is تصديق دخول اللجنة
                if person.committe_status_code_id not in [20,30,99]:                                # حاله الفرد مسجل او مصدق دخول اللجنة
                    raise Exception(f'لا يمكن تغير حاله الفرد {person.committe_status_code.afr_comm_status_name}')
                person.committe_status_code_id = new_status
                person.conf_user_id = self.request.user.pk
                person.conf_date = timezone.now()
                person.save()

            elif new_status == 99:          # new status is عدم تصديق دخول اللجنة 
                if person.committe_status_code_id not in [20,30,40,99]:                                # حاله الفرد مراجع او مصدق او منتظر انعقاد اللجنة
                    raise Exception(f'لا يمكن تغير حاله الفرد {person.committe_status_code.afr_comm_status_name}')
                person.committe_status_code_id = new_status
                person.conf_user_id = self.request.user.pk
                person.conf_date = timezone.now()
                person.save()
            
            elif new_status == 40:                              # منتظر انعقاد اللجنة
                if person.committe_status_code_id not in [20,30,40]:                                # حاله الفرد مراجع او مصدق او منتظر انعقاد اللجنة
                    raise Exception(f'لا يمكن تغير حالة الفرد {person.committe_status_code.afr_comm_status_name}')
                
                if lagna_spacific.start_date == lagna_spacific.end_date :
                    person.person_committe_date = lagna_spacific.end_date
                else:
                    # should set waiting_date in post data
                    waiting_date = request.data.get('waiting_date')
                    if not waiting_date:
                        raise ValidationError('waiting_date not set')
                #------------------------------------------------------------
                # the waiting date should be in range start <= waiting >= end
                #------------------------------------------------------------
                    start_date = lagna_spacific.start_date.date()
                    end_date=lagna_spacific.end_date.date()
                    waiting_date=timezone.make_aware(datetime.strptime(waiting_date,'%Y-%m-%d'))
                    range_date = [
                        (start_date + timedelta(days=i))
                        for i in range((end_date-start_date).days + 1)
                    ]
                    if waiting_date.date() not in range_date:
                        raise ValidationError({'error':f'the waiting date should be in range {range_date}'})

                    person.person_committe_date = waiting_date

                # set status to be waiting to lagna
                person.committe_status_code_id = new_status           # منتظر انعقاد اللجنة
                person.committe_user_date_id = self.request.user.pk
                person.save()
                
            elif new_status in [50,60]:                                 # حضور او عدم الحضور 
                if person.committe_status_code_id not in  [40,70]: 
                    raise Exception(f'لا يمكن تغير حاله الفرد {person.committe_status_code.afr_comm_status_name}')
                person.committe_status_code_id = new_status
                
                person.attend_user_id = self.request.user.pk
                person.attend_user_date = timezone.now()
                person.save()
                
            elif new_status in [70]:
                if person.committe_status_code_id not in  [50]: 
                    raise Exception(f'لا يمكن تغير حاله الفرد {person.committe_status_code.afr_comm_status_name}')
                person.committe_status_code_id = new_status
                person.save()

            serializer = LagnaStatusSerializer(person.committe_status_code)
            return Response(serializer.data)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({'details':str(e)},status=status.HTTP_400_BAD_REQUEST)





class LagnaPersonOpinionMixin:
    @transaction.atomic
    @action(detail=True,methods=['post'],permission_classes = [AllowToSetOpinion],url_path='set-opinion')
    def set_opinion(self,request,pk=None):
        try:
            user = self.request.user
            instance = self.get_object()
            data = self.request.data.copy()
            # print(data)
            data['person_id'] = instance.pk
            serializer = LagnaPersonOpinionSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            opinion_code = serializer.validated_data.get('opinion_code')
            opinion_type = serializer.validated_data.get('opinion_type')

            query = LagnaPersonsOpinions.objects.filter(opinion_code_id = opinion_code.pk , opinion_type_id = opinion_type.pk,person_id = instance.pk)
            query.update(active_flag=False)
            serializer.save(create_user=user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    @action(detail=False,methods=['get'],url_path='opinion-type')
    def get_opinion(self,request,pk=None):
        try:
            query=OpinionType.objects.all()
            serializer = OpinionTypeSerializer(query,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
            
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)














class GetVoteMemberMixin:
    @action(detail=False,methods=['get'],url_path='member-user')
    def get_member(self,request,pk=None):
        try:
            # users = User.objects.filter(groups__name = 'voter')
            group = Group.objects.get(name='voter')
            users=group.user_set.all()
            serializer =  UserSerializerBasic(users,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['get'],url_path='member-type')
    def get_member_type(self,request,pk=None):
        try:
            types = LagnaMemberType.objects.all()
            serializer =LagnaMemberTypeSerializer(types,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class AddPersonMixin:
    @action(detail=True, methods=['post'],permission_classes = [AllowToAddOrEditPerson] , url_path='person')
    def set_unit_opinion(self, request, pk=None):
        try:
            # primary key of lagna
            instance = self.get_object()
            data = {
                'mil_ser' : self.request.data.get('mil_ser'),
                'committe_code': instance.pk,
                'add_user': self.request.user.pk
            }
            serializer = LagnaPersonSerializerDetails(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(add_user=self.request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)







# class SetReviewMixin:
#     @transaction.atomic
#     @action(detail=True, methods=['post'], permission_classes = [AllowToSetReview] ,url_path='set-review')
#     def set_review(self, request, pk=None):
#         try:
#             instance = self.get_object()
#             if instance.committe_status_code_id == 20:
#                 return Response({"error": "Review already done"}, status=400)
#             if not instance.unit_opinion or not instance.army_opinion:
#                 return Response({'error': 'Unit and Army Opinion Not Set'})
#             if instance.committe_code.committe_category_id == 1 and not instance.afr_opinion:           # if it is main committe the afr hayaa should set afr opinion   
#                 return Response({'error':f'Afr opinion not set lagna is {instance.committe_code.committe_category}'})
            

#             instance.committe_status_code_id = 20
#             instance.review_user = request.user
#             instance.review_date = timezone.now()
#             instance.save()
#             return Response({"message": "Review set successfully"}, status=200)
#         except Exception as e:
#             return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


# class SetConfMixin:
#     @transaction.atomic
#     @action(detail=True, methods=['post'], permission_classes = [AllowToSetConf] ,url_path='set-conf')
#     def set_conf(self, request, pk=None):
#         try:
#             instance = self.get_object()
#             #----------------------------------------------------------------------------------------------------
#             # set committe status code to 30 -> تصديق دخول اللجنة if     20 -> تم المراجعة 
#             #                                                              99 -> لم يصدق علي دخول اللجنة
#             #----------------------------------------------------------------------------------------------------
#             if  instance.committe_status_code_id not in [20,99]:
#                 return Response({'error':"this person is not reviewd or not conf"},status=status.HTTP_400_BAD_REQUEST)

#             #-------------------------
#             # set conf and user and date
#             #-------------------------
#             instance.committe_status_code_id = 30       # تصديق دخول اللجنة
#             instance.conf_user = request.user
#             instance.conf_date = timezone.now()
#             instance.save()
#             return Response({"message": "Review set successfully"}, status=200)
#         except Exception as e:
#             return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


# class SetNotConfMixin:
#     @transaction.atomic
#     @action(detail=True, methods=['post'],permission_classes = [AllowToSetConf], url_path='set-not-conf')
#     def set_not_conf(self, request, pk=None):
#         try:
#             instance = self.get_object()
#             #----------------------------------------------------------------------------------------------------
#             # set committe status code to 99 -> تصديق دخول اللجنة if    20 -> تم المراجعة 
#             #                                                            30 -> لم يصدق علي دخول اللجنة
#             #----------------------------------------------------------------------------------------------------
#             if  instance.committe_status_code_id not in [20,30]:
#                 return Response({'error':"this person is not reviewd or not conf"},status=status.HTTP_400_BAD_REQUEST)

#             #-------------------------
#             # set conf and user and date
#             #-------------------------
#             instance.committe_status_code_id = 99      # لم يصديق دخول اللجنة 
#             instance.conf_user = request.user
#             instance.conf_date = timezone.now()
#             instance.save()
#             return Response({"message": "Review set successfully"}, status=200)
#         except Exception as e:
#             return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


# class setWatingDateMixin:
#     @transaction.atomic
#     @action(detail=True, methods=['post'], permission_classes = [AllowToSetWaitingDate] ,url_path='set-waiting-date')
#     def set_waiting_date(self, request, pk=None):
#         try:
#             instance = self.get_object()
#             #--------------------------------------------------------
#             # person status should be   20  => تم مراجعتة 
#             #                           40  => منتظر انعقاد اللجنة
#             #                           99  => لم يصدق علي دخول اللجنة
#             #--------------------------------------------------------
#             if not (instance.committe_status_code_id in [20,99,40 ]):
#                 return Response({"error": "this person is not reviewd or not conf"}, status=status.HTTP_400_BAD_REQUEST)
            
#             #--------------------------------------------------------
#             # if lagna start date = end date so it is only one day
#             #--------------------------------------------------------
#             if instance.committe_code.committe_start_date ==  instance.committe_code.committe_end_date :
#                 instance.person_committe_date = instance.committe_code.committe_end_date
#             else:
#                 # should set waiting_date in post data
#                 waiting_date = request.data.get('waiting_date')
#                 if not waiting_date:
#                     return Response({'error':'waiting_date not set'},status=status.HTTP_400_BAD_REQUEST)
#             #------------------------------------------------------------
#             # the waiting date should be in range start <= waiting >= end
#             #------------------------------------------------------------
#                 start_date = instance.committe_code.committe_start_date.date()
#                 end_date= instance.committe_code.committe_end_date.date()
#                 waiting_date=timezone.make_aware(datetime.strptime(waiting_date,'%Y-%m-%d'))
#                 range_date = [
#                     (start_date + timedelta(days=i))
#                     for i in range((end_date-start_date).days + 1)
#                 ]
#                 if waiting_date.date() not in range_date:
#                     return Response({'error':f'the waiting date should be in range {range_date}'})

#                 instance.person_committe_date = waiting_date

#             # set status to be waiting to lagna
#             instance.committe_status_code_id = 40           # منتظر انعقاد اللجنة
#             instance.save()
#             return Response({"message": "Set waiting date successfully"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


# class VoteMixin:
#     @transaction.atomic
#     @action(detail=True, methods=['post'],permission_classes = [] , url_path='vote')
#     def vote(self,request):
#         try:
#             committe_id = self.request.data.get('committe_id')
#             vote = self.request.data.get('committe_id')
#             if not (committe_id and vote):
#                 return Response({'error':f'should set committe {committe_id} and vote {vote}'})

#             person = self.get_object()
#             user = self.request.user
#             lagna= Lagna.objects.get(pk=committe_id) 
#             person_in_lagna=lagna.lagna_persons.get(mil_ser=person.mil_ser)
#             # user_in_lagna = lagna.lagna_member.get(member_id = user.)
#             if person_in_lagna.committe_status_code_id != 40:
#                 return Response({'error':f'can not set vote for this person cause its status is {person_in_lagna.committe_status_code_id}'},status=status.HTTP_400_BAD_REQUEST)
            

#         except Exception as e:
#             transaction.set_rollback(True)
#             return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)








# class BulkReviewMixin:
#     @transaction.atomic
#     @action(detail=False, methods=['post'], permission_classes=[AllowToSetReview], url_path='bulk-review')
#     def bulk_review(self, request):
#         try:
#             ids = request.data.get('ids', [])
#             if not ids:
#                 return Response({"error": "No IDs provided"}, status=400)

#             qs = self.get_queryset().filter(pk__in=ids)
#             now = timezone.now()
#             updated_count = 0
#             errors = []

#             for obj in qs:

#                 if obj.committe_status_code_id == 20:
#                     errors.append({"error": "Review already done",'mil_ser':obj.mil_ser.mil_ser})
#                     continue
#                 if not obj.unit_opinion or not obj.army_opinion:
#                     errors.append({'error': 'Unit and Army Opinion Not Set','mil_ser':obj.mil_ser.mil_ser})
#                     continue
#                 if obj.committe_code.committe_category_id == 1 and not obj.afr_opinion:           # if it is main committe the afr hayaa should set afr opinion   
#                     errors.append({'error':f'Afr opinion not set lagna is {obj.committe_code.committe_category.category_name}','mil_ser':obj.mil_ser.mil_ser})
#                     continue

#                 obj.committe_status_code_id = 20
#                 obj.review_user = request.user
#                 obj.review_date = now
#                 obj.save()
#                 updated_count += 1

#             return Response({"message": f"Review set for {updated_count} records",'count':qs.count(),'success_count':updated_count,'failer_count':len(errors),'errors':errors}, status=200)
#         except Exception as e:
#             return Response({'error':str(e)})



#     @transaction.atomic
#     @action(detail=False, methods=['post'],permission_classes=[AllowToAddOrEditPerson], url_path='bulk-delete')
#     def bulk_delete(self, request):
#         ids = request.data.get('ids', [])
#         if not ids:
#             return Response({"error": "No IDs provided"}, status=400)

#         qs = self.get_queryset().filter(pk__in=ids)
#         now = timezone.now()
#         count = qs.update(delete_flag=True, delete_user=request.user, delete_date=now)

#         return Response({"message": f"Soft deleted {count} records"}, status=200)




   