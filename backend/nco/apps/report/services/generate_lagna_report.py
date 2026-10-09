from django.db.models import Count,Q,Sum
from apps.report.models import LagnaAfrReport
from apps.report.serializers import LagnaAfrReportSerializer
from apps.tanzem.models import ArmyParentChild


def generate_lagna_report_by(filter:dict=None,group_by:list=None,output_fields:list=None):

    queryset = LagnaAfrReport.objects.filter(**filter)

    if not output_fields:
        output_fields=group_by
        if len(output_fields) == 0:
            output_fields = [ field.name for field in LagnaAfrReport._meta.fields]

    
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

    report = list(
        queryset
        .values(*group_by)
        .annotate( **{field:Sum(field) for field in sum_fields})
        .values(*output_fields,*sum_fields)
    )
    totals = queryset.aggregate( **{field : Sum(field) for field in sum_fields} )
    totals['person_army_name'] = 'الاجمالي'
    # totals['person_prnt_army_name'] = 'الاجمالي'
    report.append(totals)

    return report
    



def generate_lagna_report(committe_code,event=None):

    queryset = LagnaAfrReport.objects.filter(committe_code=committe_code)
    
    report_detail = list(LagnaAfrReportSerializer(queryset,many=True).data)

    group_fields = ['committe_name','type_name']
    output_fields = ['type_name']
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

    rep_per_comm = list(queryset.values(*group_fields).annotate(
        **{ field : Sum(field) for field in sum_fields}
    ).values(*output_fields,*sum_fields))
    totals = queryset.aggregate(
        **{field : Sum(field) for field in sum_fields}
    )
    total_row = {
        'committe_name':'الاجمالي',
        **totals
    }

    rep_per_comm.append(total_row)

    data = {
        'report_abbr':rep_per_comm,
        'report_detail':report_detail
    }
    if event:
        data['event'] = event
    data
    return data