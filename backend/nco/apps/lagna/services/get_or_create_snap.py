
from django.db import transaction
from apps.lagna.models import (
    LagnaPersons,
    LagnaAfrSnapData,
)





def get_or_create_snap(person:LagnaPersons,request=None):
    afr_data =person.mil_ser 
    
    # Anchor Calculation
    mil_ser_id = afr_data.mil_ser
    comm_type_id =person.committe_type_code.committe_type_id
    current_lagna =person.committe_type_code.committe_code
    root_comm_id = current_lagna.main_committe_code_id or current_lagna.pk

    with transaction.atomic():
        # Get or Create the Shared Snap
        snap_instance, _ = LagnaAfrSnapData.objects.get_or_create(
            mil_ser_id=mil_ser_id,
            committe_type_id=comm_type_id,
            root_committe_id=root_comm_id,
            active_flag=True,
            defaults={
                'unit_name': afr_data.unit_name, # Automated
                'unit_code': afr_data.unit_code, # Automated
                'army_code_id': afr_data.army_code, # Automated
                'prnt_army_code_id': afr_data.prnt_army_code,
                'degree_code': afr_data.degree_code_id,
                'to_unit_date': afr_data.to_unit_date ,
                'create_user': request.user if request else None
            }
        )
        return snap_instance