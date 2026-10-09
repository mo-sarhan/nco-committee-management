from django.core.management.base import BaseCommand
from django.conf import settings
from apps.photos.models import PhotoInfo,PhotoType
from apps.person.models import AfrPerson
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
                query = list()
                for row in reader:
                    try:
                        mil_ser = AfrPerson.objects.get(pk=int(row['mil_ser']))
                        small_type = PhotoType.objects.get(pk=1)
                        large_type = PhotoType.objects.get(pk=2)
                        family_type = PhotoType.objects.get(pk=3)
                        small_photo = row['small_photo']
                        large_photo = row['large_photo']
                        family_photo = row['family_photo']
                        
                        

                        
                        if small_photo:
                            query.append(PhotoInfo(mil_ser=mil_ser,photo_person_degree_code=mil_ser.degree_code, photo_type_code=small_type, photo_path=small_photo))

                        if large_photo:
                            query.append(PhotoInfo(mil_ser=mil_ser,photo_person_degree_code=mil_ser.degree_code, photo_type_code=large_type, photo_path=large_photo))
                            
                        if family_photo:
                            query.append(PhotoInfo(mil_ser=mil_ser,photo_person_degree_code=mil_ser.degree_code, photo_type_code=family_type, photo_path=family_photo))


                        counter +=1
                        self.stdout.write(self.style.SUCCESS(f"\r{counter}"),ending="")


                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'\n{str(e)}'))
                        continue
                chunck_size = 500
                for i in range(0,len(query),chunck_size):
                    PhotoInfo.objects.bulk_create(query )
                self.stdout.write(self.style.SUCCESS(f"Done...."))

                
        