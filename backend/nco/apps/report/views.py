from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db import models
from .paginators import CustomReportPaginator
from .serializers import (
    PrntPhotoReportSerializer,
    LagnaAfrReportSerializer,
)
from apps.tanzem.models import ArmyParentChild
from .mixins import UnitPhotoReportMixin,AfrPhotoReportMixin
from .models import (
    PrntPhotoReport, 
    UnitPhotoReport,
    AfrPhotoReport,

    LagnaAfrReport,
)


# class PhotoReportViewSet(ModelViewSet):
#     permission_classes  = [IsAuthenticated]
#     pagination_class = CustomReportPaginator
#     serializer_class = PrntPhotoReportSerializer
#     http_method_names = ['get']

#     def get_queryset(self):
#         user = self.request.user
#         condition = Q()
#         if not user.is_superuser:
#             condition = Q(prnt_army_code = user.profile.prnt_army_code)

#         filter_keys = self.request.query_params
#         model_fields = set(field.name for field in PrntPhotoReport._meta.fields)
        
#         for field_name,field_value in filter_keys.items():
#             if field_name in model_fields and field_value:
#                 field = PrntPhotoReport._meta.get_field(field_name)
#                 if isinstance(field,models.CharField):
#                     condition &=Q(**{f'{field_name}__icontains':field_value})
#                 elif isinstance(field,models.ForeignKey):
#                     condition &=Q(**{f'{field_name}__id':field_value})
#                 elif isinstance(field,models.IntegerField):
#                     condition &=Q(**{f'{field_name}__exact':field_value})
#         return PrntPhotoReport.objects.filter(condition)


from django.db.models import Sum
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db import models

class PhotoReportViewSet(
    AfrPhotoReportMixin,
    UnitPhotoReportMixin,
    ModelViewSet
    ):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomReportPaginator
    serializer_class = PrntPhotoReportSerializer
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        condition = Q()

        if not(user.is_superuser or user.has_perm('report.can_see_all_army')):
            prnt_army_condition= Q(prnt_army_code=user.profile.prnt_army_code_id)
            child_codes = set(ArmyParentChild.objects.filter(parent_code = user.profile.prnt_army_code_id).values_list('child_code',flat=True))
            # print(child_codes)
            child_condition = Q(prnt_army_code__in =child_codes)
            condition &= Q(Q(prnt_army_condition)|Q(child_condition))
            # condition =child_condition

        filter_keys = self.request.query_params
        model_fields = set(field.name for field in PrntPhotoReport._meta.fields)

        for field_name, field_value in filter_keys.items():
            if field_name in model_fields and field_value:
                field = PrntPhotoReport._meta.get_field(field_name)
                if isinstance(field, models.CharField):
                    condition &= Q(**{f'{field_name}__icontains': field_value})
                elif isinstance(field, models.IntegerField):
                    condition &= Q(**{f'{field_name}__exact': field_value})

        # print('############',condition)
        return PrntPhotoReport.objects.filter(condition)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # fields to sum
        sum_fields = [
            'total',
            'completed',
            'un_completed',
            'checked',
            'un_checked',
            'approved',
            'not_approved',
            'rest',
        ]

        # paginate first
        page = self.paginate_queryset(queryset)

        # serialize page data
        serializer = self.get_serializer(page, many=True)
        data = list(serializer.data)

        paginator = self.paginator

        # 🔥 ONLY last page → add total row
        if paginator.page.number == paginator.page.paginator.num_pages:
            totals = queryset.aggregate(
                **{field: Sum(field) for field in sum_fields}
            )
            totals = {k: v or 0 for k, v in totals.items()}

            total_row = {
                "prnt_army_code": None,
                "prnt_army_name": "total",
                **totals
            }

            data.append(total_row)

        return paginator.get_paginated_response(data)




class LagnaAfrReportViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomReportPaginator
    serializer_class = LagnaAfrReportSerializer
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        queryset = LagnaAfrReport.objects.all()

        if not(user.is_superuser or user.has_perm('report.can_see_all_army')):
            child_codes = set(ArmyParentChild.objects.filter(parent_code = user.profile.prnt_army_code_id).values_list('child_code',flat=True))
            queryset = queryset.filter(Q(prnt_army_code = user.profile.prnt_army_code_id)| Q(prnt_army_code__in = child_codes))

        filter_keys = self.request.query_params
        model_fields = set(field.name for field in LagnaAfrReport._meta.fields)

        for field_name, field_value in filter_keys.items():
            if field_name in model_fields and field_value:
                field = LagnaAfrReport._meta.get_field(field_name)
                if isinstance(field, models.CharField):
                    queryset=queryset.filter(**{f'{field_name}__icontains': field_value})
                elif isinstance(field, models.IntegerField):
                    queryset=queryset.filter(**{f'{field_name}__exact': field_value})

        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # fields to sum
        sum_fields = [
            'total',
            'st_10',
            'st_20',
            'st_30',
            'st_40',
            'st_50',
            'st_60',
            'st_70',
            'st_99'
        ]

        # paginate first
        page = self.paginate_queryset(queryset)

        # serialize page data
        serializer = self.get_serializer(page, many=True)
        data = list(serializer.data)

        paginator = self.paginator

        # 🔥 ONLY last page → add total row
        if paginator.page.number == paginator.page.paginator.num_pages:
            totals = queryset.aggregate(
                **{field: Sum(field) for field in sum_fields}
            )
            totals = {k: v or 0 for k, v in totals.items()}

            total_row = {
                "prnt_army_code": None,
                "prnt_army_name": "الاجمالي",
                **totals
            }

            data.append(total_row)

        return paginator.get_paginated_response(data)