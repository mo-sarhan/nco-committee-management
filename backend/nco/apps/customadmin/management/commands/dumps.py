from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.apps import apps
from django.core.paginator import Paginator
from django.db import transaction,connections
import time

class Command(BaseCommand):
    help = "Oracle → SQLite migrator: tables, materialized views, views (handles external dependencies)"

    def add_arguments(self, parser):
        parser.add_argument("--source", default="oracledb")
        parser.add_argument("--distination", default="default")
        parser.add_argument("--truncate", action="store_true")
        parser.add_argument("--resume", action="store_true")
        parser.add_argument("--models",type=str,help='only dump this models')

    def handle(self, *args, **options):
        start_time = time.perf_counter()
        CHUNK_SIZE = 7000
        models_to_dump = options['models']
        source_db:str = options['source']
        distination_db:str = options['distination']
        models = []

        if models_to_dump:
            app_label,model = models_to_dump.split('.')
            models.append(apps.get_model(app_label,model))
        else:
            models = apps.get_models()
        
        if 'sqlite' in distination_db.strip().lower():
            with connections[distination_db].cursor() as cursor:
                cursor.execute('PRAGMA foreign_keys = OFF;')
        if 'postgre' in distination_db.strip().lower():
            with connections[distination_db].cursor() as cursor:
                cursor.execute("SET session_replication_role = 'replica';")

        models.reverse()
        try:
            for model in models:
                total = 0
                self.stdout.write(self.style.SUCCESS(f'{model._meta.db_table} : {model._meta.model_name}'))
                if model._meta.model_name in ['profile','armycode','rank','armyparentchild','afrdegree','familydegreecode']:
                    continue
                queryset = None
                if model._meta.model_name in ['afrperson','lagna','afrsnapopinion','afrsecuritysituation','lagnapersons']:
                    queryset = model.all_objects.using(source_db).all().order_by('pk')
                    distination_query = model.all_objects.using(distination_db).all()
                else:
                    queryset = model.objects.using(source_db).all().order_by('pk')
                    distination_query = model.objects.using(distination_db).all()

                queryset_count = queryset.count()
                distination_query_count = distination_query.count()
                if queryset_count == distination_query_count:
                    self.stdout.write(self.style.WARNING(f'{model._meta.db_table} : {model._meta.model_name} SKIPPED source:{queryset_count} destination:{distination_query_count}'))
                    continue
                    
                    

                paginator = Paginator(queryset,CHUNK_SIZE)
                with transaction.atomic(using=distination_db):
                    for page_num in paginator.page_range:
                        try:
                            page = paginator.page(page_num)
                            model.objects.using(distination_db).bulk_create(list(page.object_list),ignore_conflicts=True)
                            total +=CHUNK_SIZE
                            self.stdout.write(self.style.SUCCESS(f'\r{page_num} / {paginator.num_pages} / {page_num * CHUNK_SIZE} / {queryset_count}'),ending='')
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'{e}'),ending='\n')
                            continue
                    self.stdout.write('\n')
        finally:
            if 'sqlite' in distination_db.strip().lower():
                with connections[distination_db].cursor() as cursor:
                    cursor.execute('PRAGMA foreign_keys = ON;')
            if 'postgre' in distination_db.strip().lower():
                with connections[distination_db].cursor() as cursor:
                    cursor.execute("SET session_replication_role = 'origin';")
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        hours , remainder = divmod(elapsed,3600)
        minutes , seconds = divmod(remainder,60)
        self.stdout.write(self.style.SUCCESS(f'Dumping take {int(hours)}h :{int(minutes)}m :{int(seconds)}s'))
        