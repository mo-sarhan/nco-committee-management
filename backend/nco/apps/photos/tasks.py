# create background task to calcualte the person images
# At the end of the image , a report will be send through websocket
from requests.exceptions import RequestException
from apps.photos.services.check_nsfw_photo import check_nsfw
import time
from celery import shared_task
from apps.photos.models import PhotoInfo
from apps.report.models import AfrPhotoReport
from apps.report.utilties import send_websocket_report
from django.conf import settings


@shared_task
def calculate_person_photos(photo_id: int):
    photo = PhotoInfo.objects.get(pk=photo_id)

    person = photo.mil_ser
    family = person.family

    photos = person.photos.filter(active_flag=True, delete_flag=False)
    half_photo = photos.filter(photo_type_code_id=1).exists()
    tall_photo = photos.filter(photo_type_code_id=2).exists()
    family_photos = photos.filter(photo_type_code_id=3)

    marital_status = True if person.marital_state_code in [
        15, 1] else False  # if its status متزوج او متزوج و يعول

    family_status = False
    if marital_status:
        wifies_num = family.get_curr_wifies().count()
        family_status = True if wifies_num == family_photos.count() else False
    else:
        sons_lives = family.get_live_children().exists()
        family_status = True if sons_lives and (
            family_photos.count() > 0) else False

    completed_flag = all([half_photo, tall_photo, family_status])

    checked_flag = not photos.filter(photo_status=0).exists()
    approved_flag = not photos.filter(photo_status=2).exists()

    AfrPhotoReport.objects.update_or_create(mil_ser=person,
                                            defaults={
                                                'completed_flag': completed_flag,
                                                'checked_flag': checked_flag,
                                                'approved_flag': approved_flag
                                            })

    # at the end we should send the report via websocket

    group_name = f'photo_report_{person.prnt_army_code}'

    # print('group_name',group_name)
    send_websocket_report(person.prnt_army_code, group_name)
    send_websocket_report(None, 'photo_report')


@shared_task(
    bind=True,
    max_retries=5,
)
def check_photo_nsfw(self, photo_id):

    try:
        photo = PhotoInfo.objects.get(pk=photo_id)

        with photo.photo_path.open("rb") as file:

            result = check_nsfw(file)

        photo.is_nsfw = result['data']["is_nsfw"]

        PhotoInfo.objects.filter(pk=photo_id).update(is_nsfw=result['data']['is_nsfw'])

        return {
            "photo_id": photo_id,
            "is_nsfw": photo.is_nsfw,
        }

    except RequestException as exc:

        raise self.retry(
            exc=exc,
            countdown=min(60 * (2 ** self.request.retries), 600),
        )
