from django.db import models
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import (
    ArmyCode,
    Rank,
)
from .serializers import (
    ArmyCodeSerializer,
    RankSerializer,
)



class RankViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RankSerializer
    http_method_names = ['get']
    queryset = Rank.objects.all()
    lookup_field = 'rank_code'

# Create your views here.
class ArmyCodeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ArmyCodeSerializer
    queryset = ArmyCode.objects.all()
    http_method_names = ['get']
    limit_query_count = 10

    def get_queryset(self):
        query = ArmyCode.objects.all()

        filter_keys = self.request.query_params
        model_fields = set(field.name for field in ArmyCode._meta.fields)
        # final_field = set(field for field in  filter_keys.keys() if field in model_keys  )
        # condition = Q(delete_flag=False,active_flag=True)
        condition = Q()
        
        for field_name,field_value in filter_keys.items():
            if field_name in model_fields and field_value:
                field = ArmyCode._meta.get_field(field_name)
                if isinstance(field,models.CharField):
                    condition &=Q(**{f'{field_name}__icontains':field_value})
                elif isinstance(field,models.ForeignKey):
                    condition &=Q(**{f'{field_name}__id':field_value})
                elif isinstance(field,models.IntegerField):
                    condition &=Q(**{f'{field_name}__exact':field_value})

        query = query.filter(condition)
        
        if query.count() >= self.limit_query_count:
            query = query[:self.limit_query_count]
        return query
