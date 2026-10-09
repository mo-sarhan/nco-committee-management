# from django.db.models import Count, Q, Max, F, Case, When, IntegerField,Sum
# from apps.report.models import PrntPhotoReport
# from apps.report.serializers import PrntPhotoReportSerializer
# from apps.tanzem.models import ArmyParentChild
# import json

# def generate_photo_report(prnt_army_code):

#     condition=Q()
#     if prnt_army_code:
#         child_codes = set(ArmyParentChild.objects.filter(parent_code = prnt_army_code).values_list('child_code',flat=True))
#         # print(child_codes)
#         # child_condition = Q(prnt_army_code__in =child_codes)
#         condition &=Q(Q(prnt_army_code=prnt_army_code)|Q(prnt_army_code__in = child_codes))
#     # print(condition)
#     queryset = PrntPhotoReport.objects.filter(condition)
#     serializer = PrntPhotoReportSerializer(queryset,many=True)
#     data = list(serializer.data)
#     sum_fields = [
#         'total',
#         'completed',
#         'un_completed',
#         'checked',
#         'un_checked',
#         'approved',
#         'not_approved',
#         'rest',
#     ]

#     totals = queryset.aggregate(
#         **{field: Sum(field) for field in sum_fields}
#     )
#     totals = {k: v or 0 for k, v in totals.items()}

#     total_row = {
#         "prnt_army_code": None,
#         "prnt_army_name": "total",
#         **totals
#     }

#     data.append(total_row)
#     json_data = json.dumps(data)
#     # return json_data
#     return data

    
    
from django.db.models import Q, Sum

from apps.report.models import PrntPhotoReport
from apps.report.serializers import PrntPhotoReportSerializer
from apps.tanzem.models import ArmyParentChild


def generate_photo_report(prnt_army_code=None):

    queryset = PrntPhotoReport.objects.all()

    if prnt_army_code:
        child_codes = (
            ArmyParentChild.objects
            .filter(parent_code=prnt_army_code)
            .values_list("child_code", flat=True)
        )

        queryset = queryset.filter(
            Q(prnt_army_code=prnt_army_code)
            | Q(prnt_army_code__in=child_codes)
        )

    data = list(
        PrntPhotoReportSerializer(
            queryset,
            many=True
        ).data
    )

    sum_fields = [
        "total",
        "completed",
        "un_completed",
        "checked",
        "un_checked",
        "approved",
        "not_approved",
        "rest",
    ]

    totals = queryset.aggregate(
        **{
            field: Sum(field)
            for field in sum_fields
        }
    )

    totals = {
        key: value or 0
        for key, value in totals.items()
    }

    data.append({
        "prnt_army_code": None,
        "prnt_army_name": "total",
        **totals,
    })

    return data



