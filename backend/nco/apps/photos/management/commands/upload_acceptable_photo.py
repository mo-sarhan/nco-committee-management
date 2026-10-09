from django.core.management.base import BaseCommand
from django.conf import settings
from apps.photos.models import PhotoInfo,PhotoType,PhotoStatusType
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
                for row in reader:
                    try:
                        mil_ser = AfrPerson.objects.get(pk=int(row['mil_ser']))
                        mil_ser.photos.update(photo_status_id = 1)
                        counter +=1
                        self.stdout.write(self.style.SUCCESS(f"\r{counter}"),ending="")

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'\n{str(e)}'))
                        continue

                
        