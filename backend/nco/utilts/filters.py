from django.db import models
from django.db.models import Q

def get_filter_cond(model,params,query):
    model_fields = set(field.name for field in model._meta.fields)
    for field_name,field_value in params.items():
        if field_name in model_fields and field_value:
            field = model._meta.get_field(field_name)
            if isinstance(field,models.CharField):
                query=query.filter(Q(**{f'{field_name}__icontains':field_value}))
            elif isinstance(field,models.ForeignKey):
                query=query.filter(Q(**{f'{field_name}__id':field_value}))
            elif isinstance(field,models.IntegerField):
                query =query.filter(Q(**{f'{field_name}__exact':field_value}))
    return query