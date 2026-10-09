from django.db import transaction
from ..models import Lagna
from ..serializers import (
    CreateLagnaSerializerBasic
)


@transaction.atomic
def create_lagna(request,instance:None):
    data=request.data.copy()
    data['committe_create_user'] = request.user.pk
    serializer = None
    if instance:
        serializer = CreateLagnaSerializerBasic(instance,data=data)
    else:
        serializer = CreateLagnaSerializerBasic(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data
    return serializer.errors
