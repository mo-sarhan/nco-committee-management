
from django.db import transaction
from django.db.models import Q
from apps.person.models import AfrPerson

@transaction.atomic
def get_persons(filter_condition):
    filter_keys = set(filter_condition.keys())
    model_keys= set(field.name for field in AfrPerson._meta.fields)
    un_found_keys = filter_keys - model_keys

    if len(un_found_keys) > 0:
        raise Exception({"error":f"can not found {un_found_keys} field in AfrPerson"})

    condition = Q()
    for key , value in filter_condition.items():
        condition &=Q(**{f'{key}__icontains':value})
    return AfrPerson.objects.filter(condition)

@transaction.atomic
def get_person_details(pk):
    condition = Q(pk=pk)
    return AfrPerson.objects.filter(pk=pk)
