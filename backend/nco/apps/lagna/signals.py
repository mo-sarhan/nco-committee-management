from django.db.models.signals import post_save
from apps.lagna.models import LagnaPersons,AfrSnapOpinion
from apps.lagna.services.get_or_create_snap import get_or_create_snap
from django.dispatch import receiver


@receiver(post_save,sender=LagnaPersons)
def create_user_profile(sender,instance,created,**kwargs):
    snap=get_or_create_snap(instance)
    if created:
        opinions = {
            'army_opinion':AfrSnapOpinion(snap_id=snap,opinion_type_id = 3,opinion_code=None),
            'hayaa_opinioni':AfrSnapOpinion(snap_id=snap,opinion_type_id = 7,opinion_code=None),
        }
        if (snap.army_code and snap.prnt_army_code) and (snap.army_code != snap.prnt_army_code):
            opinions['prnt_opinion'] = AfrSnapOpinion(snap_id=snap,opinion_type_id = 2,opinion_code=None)
        AfrSnapOpinion.objects.bulk_create(opinions.values())
    

