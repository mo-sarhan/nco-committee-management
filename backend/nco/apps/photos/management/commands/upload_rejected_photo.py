from django.core.management.base import BaseCommand
from django.conf import settings
from apps.photos.models import PhotoInfo,PhotoType,RejectPhotoInfo,RejectPhotoReason,PhotoStatusType
from apps.person.models import AfrPerson
from django.contrib.auth.models import User
import csv
import os
import django as pd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            type=str,
            required=True,
            help='csv file path'

        )
    def handle(self, *args, **options):
            csv_path = options['csv']

            with open(csv_path,newline="",encoding="utf-8") as file:
                reader = csv.DictReader(file)
                counter = 0
                error_counter = 0
                query = list()
                for row in reader:
                    try:
                        #-----------------------
                        # 
                        #-----------------------
                        mil_ser =AfrPerson.objects.get(mil_ser=int(row['mil_ser']))
                        user = User.objects.get(username=row['username'])
                        photo_type_code = PhotoType.objects.get(pk=int(row['photo_code']))
                        rejected_reason = RejectPhotoReason.objects.get(pk=int(row['reason_code']))
                        date = row['date']

                        # get photo by mil_ser and type code and active
                        photo=PhotoInfo.objects.get(mil_ser=mil_ser,photo_type_code=photo_type_code,active_flag=True)
                        query.append(RejectPhotoInfo(photo_id = photo,reject_code = rejected_reason,reject_user_code=user))
                        photo.photo_status_id = 2
                        photo.review_user_id = user
                        photo.review_date =  date
                        photo.save(update_fields=['photo_status','review_user'])
                        counter +=1
                        self.stdout.write(self.style.SUCCESS(f"\r{counter}"),ending="")


                    except Exception as e:
                        error_counter+=1
                        self.stdout.write(self.style.ERROR(f'\n{error_counter}:{str(e)}'))
                        continue
                chunck_size = 500
                for i in range(0,len(query),chunck_size):
                    RejectPhotoInfo.objects.bulk_create(query[i:i+chunck_size] )
                self.stdout.write(self.style.SUCCESS(f"\nDone...."))

                
        