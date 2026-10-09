from django.db.models.signals import post_delete,post_save
from django.db.models import ManyToManyField
from .models import PhotoInfo
from django.dispatch import receiver
from .tasks import calculate_person_photos,check_photo_nsfw


@receiver(post_save,sender=PhotoInfo)
def check_person_images(sender,instance,created,**args):
    """"
    this function is made to calculate the number of the image and check user accpeted or rejected photo
    but to save response time we well make the operation made in background useing celery
    """

    calculate_person_photos.delay(instance.pk)
    check_photo_nsfw.delay(instance.pk)
