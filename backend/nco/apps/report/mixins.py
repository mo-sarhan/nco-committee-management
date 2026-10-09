from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction,models
from django.db.models import Q,Sum
from .models import UnitPhotoReport,AfrPhotoReport
from apps.person.models import AfrPerson
from .serializers import UnitPhotoReportSerializer,AfrPhotoReportSerializer
from .paginators import CustomAfrReportPaginator,CustomUnitReportPaginator



class UnitPhotoReportMixin:

    @action(detail=True,methods=['get'],url_path='units(?:/(?P<unit_code>\d+))?',pagination_class =CustomUnitReportPaginator)
    def unit_report(self,request,pk=None,unit_code=None):
        try:

            user = self.request.user
            instance = self.get_object()
            condition = Q()

            if not user.is_superuser:
                # condition = Q(prnt_army_code=user.profile.prnt_army_code_id)
                condition = Q(prnt_army_code=instance.prnt_army_code)

            # print('############',condition)
            if unit_code:
                unit = UnitPhotoReport.objects.get(condition,unit_code = unit_code)
                serializer = UnitPhotoReportSerializer(unit)
                return Response(serializer.data,status=status.HTTP_200_OK)

            filter_keys = self.request.query_params
            model_fields = set(field.name for field in UnitPhotoReport._meta.fields)

            for field_name, field_value in filter_keys.items():
                if field_name in model_fields and field_value:
                    field = UnitPhotoReport._meta.get_field(field_name)
                    if isinstance(field, models.CharField):
                        condition &= Q(**{f'{field_name}__icontains': field_value})
                    elif isinstance(field, models.IntegerField):
                        condition &= Q(**{f'{field_name}__exact': field_value})

            query = UnitPhotoReport.objects.filter(condition,prnt_army_code = instance.prnt_army_code)

            sum_fields = [
               'total' ,
               'completed' ,
               'un_completed' ,
               'checked' ,
               'un_checked' ,
               'approved',
               'not_approved',
                'rest', 
            ]

            page = self.paginate_queryset(query)
            serializer = UnitPhotoReportSerializer(page,many=True)
            data = list(serializer.data)

            paginator = self.paginator
            if paginator.page.number == paginator.page.paginator.num_pages:
                totals = query.aggregate(
                    **{field: Sum(field) for field in sum_fields}
                )
                totals = {k: v or 0 for k, v in totals.items()}

                total_row = {
                    "prnt_army_code": None,
                    "prnt_army_name": None,
                    "unit_code": None,
                    "unit_name": 'الاجمالي',
                    **totals
                }

                data.append(total_row)

            return paginator.get_paginated_response(data)

        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)



class AfrPhotoReportMixin:

    @action(detail=True,methods=['get'],url_path='units/(?P<unit_code>\d+)/persons(?:/(?P<mil_ser>\d+))?')
    def afr_report(self,request,pk=None,unit_code=None,mil_ser=None):
        try:

            user = self.request.user
            instance = self.get_object()
            unit = UnitPhotoReport.objects.get(unit_code=unit_code)
            condition = Q()

            if not user.is_superuser:
                condition = Q(mil_ser__prnt_army_code=instance.prnt_army_code)

            if mil_ser:
                person = AfrPhotoReport.objects.get(condition,mil_ser__unit_code = unit_code,mil_ser=mil_ser)
                serializer = AfrPhotoReportSerializer(person)
                return Response(serializer.data,status=status.HTTP_200_OK)

            filter_keys = self.request.query_params
            model_fields = set(field.name for field in AfrPhotoReport._meta.fields)

            for field_name, field_value in filter_keys.items():
                if field_name in model_fields and field_value:
                    field = AfrPhotoReport._meta.get_field(field_name)
                    if isinstance(field, models.CharField):
                        condition &= Q(**{f'{field_name}__icontains': field_value})
                    elif isinstance(field,models.ForeignKey):
                        condition &= Q(**{f'{field_name}': field_value})
                    elif isinstance(field,models.BooleanField):
                        condition &= Q(**{f'{field_name}': field_value})
                    elif isinstance(field, models.IntegerField):
                        condition &= Q(**{f'{field_name}__exact': field_value})
                else:
                    parts = field_name.split('__')
                    # print(field_name)
                    if len(parts) == 2:
                        rel_field_name = parts[0]
                        rel_fd_name = parts[1]
                        if rel_field_name in model_fields:
                            rel_field = AfrPhotoReport._meta.get_field(rel_field_name)
                            # print(rel_field)
                            # print(rel_field.related_model)
                            related_model_fields = [field.name for field in rel_field.related_model._meta.fields]
                            if isinstance(rel_field,models.ForeignKey) and rel_fd_name in related_model_fields:
                                rel_fd_name_type = rel_field.related_model._meta.get_field(rel_fd_name)
                                if isinstance(rel_fd_name_type,models.CharField):
                                    condition &=Q(**{f'{field_name}__icontains':field_value})
                                elif isinstance(rel_fd_name_type,models.IntegerField):
                                    condition &=Q(**{f'{field_name}__exact':field_value})

            query = AfrPhotoReport.objects.filter(condition,mil_ser__prnt_army_code = instance.prnt_army_code,mil_ser__unit_code=unit.unit_code)

            page = self.paginate_queryset(query)
            serializer = AfrPhotoReportSerializer(page,many=True)
            data = list(serializer.data)
            paginator = self.paginator

            return paginator.get_paginated_response(data)

        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True,methods=['get'],url_path='persons(?:/(?P<mil_ser>\d+))?',pagination_class = CustomAfrReportPaginator)
    def prnt_afr_report(self,request,pk=None,mil_ser=None):
        try:

            user = self.request.user
            instance = self.get_object()
            condition = Q()

            if not (user.is_superuser or user.has_perm('report.can_see_all_army')):
                condition = Q(mil_ser__prnt_army_code=instance.prnt_army_code)

            if mil_ser:
                person = AfrPhotoReport.objects.get(condition,mil_ser_id = mil_ser)
                serializer = AfrPhotoReportSerializer(person)
                return Response(serializer.data,status=status.HTTP_200_OK)

            filter_keys = self.request.query_params
            model_fields = set(field.name for field in AfrPhotoReport._meta.fields)

            for field_name, field_value in filter_keys.items():
                if field_name in model_fields and field_value:
                    # print(field_name)
                    field = AfrPhotoReport._meta.get_field(field_name)
                    if isinstance(field, models.CharField):
                        condition &= Q(**{f'{field_name}__icontains': field_value})
                    elif isinstance(field,models.ForeignKey):
                        condition &= Q(**{f'{field_name}': field_value})
                    elif isinstance(field,models.BooleanField):
                        condition &= Q(**{f'{field_name}': field_value})
                    elif isinstance(field, models.IntegerField):
                        condition &= Q(**{f'{field_name}__exact': field_value})

                else:
                    parts = field_name.split('__')
                    # print(field_name)
                    if len(parts) == 2:
                        rel_field_name = parts[0]
                        rel_fd_name = parts[1]
                        if rel_field_name in model_fields:
                            rel_field = AfrPhotoReport._meta.get_field(rel_field_name)
                            # print(rel_field)
                            # print(rel_field.related_model)
                            related_model_fields = [field.name for field in rel_field.related_model._meta.fields]
                            if isinstance(rel_field,models.ForeignKey) and rel_fd_name in related_model_fields:
                                rel_fd_name_type = rel_field.related_model._meta.get_field(rel_fd_name)
                                if isinstance(rel_fd_name_type,models.CharField):
                                    condition &=Q(**{f'{field_name}__icontains':field_value})
                                elif isinstance(rel_fd_name_type,models.IntegerField):
                                    condition &=Q(**{f'{field_name}__exact':field_value})
            query = AfrPhotoReport.objects.filter(condition,mil_ser__prnt_army_code = instance.prnt_army_code)

            page = self.paginate_queryset(query)
            serializer = AfrPhotoReportSerializer(page,many=True)
            data = list(serializer.data)

            paginator = self.paginator
            return paginator.get_paginated_response(data)

        except Exception as e:
            return Response({'detail':str(e)},status=status.HTTP_400_BAD_REQUEST)