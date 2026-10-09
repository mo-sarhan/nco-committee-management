
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.core.paginator import Paginator
from django.db import transaction,connections
from apps.person.models import AfrPerson
from apps.lagna.services.get_or_create_snap import get_or_create_snap
from apps.lagna.models import Lagna,LagnaPersons,OpinionType,AfrSnapOpinion,LagnaPersonReasons
from django.contrib.auth.models import User
from django.core.files import File
from apps.lagna.serializers import LagnaPersonSerializerBasic
import pandas as pd
import time
import os


class Command(BaseCommand):
    help = "Oracle → SQLite migrator: tables, materialized views, views (handles external dependencies)"

    def add_arguments(self, parser):
        parser.add_argument("--excel", type=str,required=True,help='excel file to upload')
        parser.add_argument("--images_path", type=str,help='excel file to upload')

    def handle(self, *args, **options):
        excel_file = options['excel']
        folder_path = options['images_path']
        root_lagna = Lagna.objects.get(pk=1)
        lagna_spacific = root_lagna.lagna_type_spacific.get(pk=123)
        admin_user = User.objects.get(username='admin')

        file = pd.read_excel(excel_file)

        file['MIL_NO']= file['MIL_NO'].astype(str)
        file['PRNT_ARMY_OPINION'] = file['PRNT_ARMY_OPINION'].astype(int)
        # file['PRNT_ARMY_REASON'] = file['PRNT_ARMY_REASON'].astype(str)
        file['ARMY_OPINION'] = file['ARMY_OPINION'].astype(int)
        # file['ARMY_REASON'] = file['ARMY_REASON'].astype(str)
        file['REASON'] = file['REASON'].astype(str)

        # upload lagna person
        with transaction.atomic():

            all_persons =file['MIL_NO'].to_list()
            lagna_persons =list(lagna_spacific.lagna_persons.filter(active_flag=True,delete_flag=False).values_list('mil_ser__mil_no',flat=True))
            all_lagna_persons = set(all_persons+lagna_persons)
            afr_persons = AfrPerson.objects.filter(mil_no__in=all_lagna_persons)

            self.stdout.write(self.style.WARNING('upload afr person to lagna'))
            counter = 0
            for person in afr_persons:
                try:
                    LagnaPersons.objects.update_or_create(mil_ser_id=person.mil_ser,committe_type_code=lagna_spacific,
                                                          defaults={
                                                              'add_user' : admin_user
                                                              })
                    self.stdout.write(self.style.SUCCESS(f'\r{root_lagna.committe_name} {lagna_spacific.committe_type.type_name} : {counter}'),ending='')
                    counter +=1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f' {person.mil_ser}'))
                    continue
                    
            self.stdout.write()
            self.stdout.write(self.style.SUCCESS(f'{lagna_spacific.lagna_persons.filter(active_flag=True,delete_flag=False).count()}'))


        # upload reasons
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('upload reasons!!!!!'))
            lagna_persons =lagna_spacific.lagna_persons.filter(active_flag=True,delete_flag=False)
            counter = 0
            for row in file.itertuples():
                person = lagna_persons.filter(mil_ser__mil_no = row.MIL_NO).first()
                if person:
                    snap_id = get_or_create_snap(person)
                    LagnaPersonReasons.objects.update_or_create(snap_id=snap_id,active_flag=True,delete_flag=False,defaults={
                        'descrption' : row.REASON,
                        'create_user': admin_user,
                    })
                    counter +=1
                    self.stdout.write(self.style.SUCCESS(f'\r reasons: {person.mil_ser.mil_no} : {counter}'),ending='')
            self.stdout.write()


        # upload opinion
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('upload opinion'))
            lagna_persons =lagna_spacific.lagna_persons.filter(active_flag=True,delete_flag=False)
            counter = 0
            attach_counter = 0
            for row in file.itertuples():
                person = lagna_persons.filter(mil_ser__mil_no = row.MIL_NO).first()
                if person:
                    snap_id = get_or_create_snap(person)
                    prnt_opinion = 2
                    army_opinion = 3
                    # snap_id.opinions.filter(opinion_type_id__in=[1]).update(active_flag=False,delete_flag=False,delete_user=admin_user)
                    # upload prnt army opinion
                    army_op,created = AfrSnapOpinion.objects.update_or_create(snap_id=snap_id,opinion_type_id=army_opinion,defaults={
                                                            # 'opinion_notes' : row.ARMY_REASON,
                                                            'opinion_code_id':row.ARMY_OPINION,
                                                            'create_user':admin_user
                                                            }
                                                            )
                    if person.mil_ser.prnt_army_code != person.mil_ser.army_code:
                        prnt_op,created = AfrSnapOpinion.objects.update_or_create(snap_id=snap_id,opinion_type_id=prnt_opinion,defaults={
                                                                # 'opinion_notes' : row.PRNT_ARMY_REASON,
                                                                'opinion_code_id':row.PRNT_ARMY_OPINION,
                                                                'create_user':admin_user
                                                                }
                                                                )

                    # filename = f'{person.mil_ser.mil_no}.jpg'
                    # file_path = os.path.join(folder_path,filename)
                    # if os.path.isfile(file_path):
                    #     with open(file_path,'rb') as attach:
                    #         prnt_op.opinion_attached.save(file_path,File(attach),save=True)
                    #         army_op.opinion_attached.save(file_path,File(attach),save=True)
                    #         snap_id.attach.save(file_path,File(attach),save=True)
                    #     attach_counter += 1
                    
                    counter +=1
                    self.stdout.write(self.style.SUCCESS(f'\r {person.mil_ser.mil_no} : {counter} / attach : {attach_counter}'),ending='')





