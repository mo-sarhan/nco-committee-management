
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.photos.models import PhotoInfo,PhotoType,RejectPhotoInfo,RejectPhotoReason,PhotoStatusType
from apps.person.models import AfrPerson
from django.contrib.auth.models import User
from apps.users.models import Profile
import csv
import os
import django as pd


class Command(BaseCommand):
    def handle(self, *args, **options):
        queryset =Profile.objects.all()
        self.stdout.write(self.style.NOTICE(f"total = {queryset.count()} "))
        counter = 0

    
        for profile in queryset:
            try:
                profile.prnt_army_code = profile.army_code
                profile.prnt_army_name = profile.army_name
                profile.save()
                counter +=1
                self.stdout.write(self.style.SUCCESS(f"\r counter : {counter}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\n{e}"))
                continue

        self.stdout.write(self.style.SUCCESS(f"\nDone...."))
            



                
        