from django.core.management.base import BaseCommand
from django.conf import settings
from apps.photos.models import PhotoInfo,PhotoType,RejectPhotoInfo,RejectPhotoReason
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
                # print('total:',reader.count())
                for row in reader:
                    try:
                        username =row['username']
                        army_code = row['army_code']
                        army_name= row['army_name']
                        # password = row['password']
                        # first_name = row['first_name']
                        # last_name = row['last_name']
                        # instance=User(username=username)
                        instance=User.objects.get(username=username)
                        # instance.set_password(password)
                        # instance.save()
                        # instance.profile.army_code = army_code
                        instance.profile.army_code_id = army_code
                        instance.profile.prnt_army_code_id = army_code
                        # instance.profile.password = password
                        instance.save()
                        # print(instance.profile.prnt_army_code_id,'\n')

                        counter +=1
                        self.stdout.write(self.style.SUCCESS(f"\r{counter}"),ending="")


                    except Exception as e:
                        error_counter+=1
                        self.stdout.write(self.style.ERROR(f'\n{error_counter} {str(e)}'))
                        continue
                
        