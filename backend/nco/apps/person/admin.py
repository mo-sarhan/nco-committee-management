from django.contrib import admin
from django.db import models
from django import forms
from django.http import HttpResponseRedirect
from apps.report.admin import AfrPhotoReportInline
from apps.photos.admin import (
    PhotoInfoInline,
)

from apps.lagna.admin import (
    LagnaPersonsInline,
)
from apps.tanzem.models import ArmyParentChild
from .models import (
    Family,
    FamilyStatistic,
    AfrPunishment,
    AfrTagdedHistroy,
    AfrPerson,
    PersonEffecincy,
    PersonEffecincyL3Y,
    PersonEffecincyAvg,
    PunishmentStatistics,
    MedicalLagnaResultLookUp,
    MedicalHistory,
    AfrEducation,
    AfrUnits,
    AfrDegree,
    AfrPsychologicalReport,
    AfrTravel,
    AfrSecuritySituation,
    AfrVacation
    )

# Register your models here.

class AfrVacationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AfrVacation._meta.fields]
    search_fields = ['mil_ser__mil_ser','mil_ser__mil_no','mil_ser__person_name']
    autocomplete_fields = ['mil_ser']
    list_filter =['mil_ser__army_name','mil_ser__prnt_army_name','mil_ser__person_sex_name']

class AfrVacationInline(admin.TabularInline):
    model = AfrVacation
    list_display = [field.name for field in AfrVacation._meta.fields]
    extra = 0

class MedicalLagnaResultLookUpAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MedicalLagnaResultLookUp._meta.fields]

class AfrSecuritySituationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AfrSecuritySituation._meta.fields]
    search_fields = ['mil_ser__mil_ser','mil_ser__mil_no','mil_ser__person_name']

class AfrSecuritySituationInline(admin.TabularInline):
    model = AfrSecuritySituation
    list_display = [field.name for field in ArmyParentChild._meta.fields]
    extra = 0



class ArmyPerentChildAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArmyParentChild._meta.fields]
    readonly_fields = [field.name for field in ArmyParentChild._meta.fields]
    search_fields = [field.name for field in ArmyParentChild._meta.fields]

class AfrDegreeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AfrDegree._meta.fields]
    fields = list_display
    readonly_fields = list_display


class AfrDegreeAdminInline(admin.ModelAdmin):
    model=AfrDegree
    fields = [field.name for field in AfrDegree._meta.fields]
    extra = 0

class FamilyInline(admin.TabularInline):
    model=Family
    fields=[ field.name for field in Family._meta.fields ]
    extra=0


class FamilyAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in Family._meta.fields]
    readonly_fields = list_display
    search_fields = ['mil_ser__mil_ser','mil_ser__mil_no','mil_ser__person_name']


class FamilyStatisticInline(admin.TabularInline):
    model=FamilyStatistic
    fields=[ field.name for field in FamilyStatistic._meta.fields ]
    extra=0



class FamilyStatisticAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in FamilyStatistic._meta.fields]
    search_fields = ['mil_ser','mil_ser__person_name']

class AfrPunishmentAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in AfrPunishment._meta.fields]
    readonly_fields = list_display
    search_fields = ['mil_ser__mil_no','mil_ser__mil_ser','mil_ser__person_name']
    list_filter = ['punsh_cort']

class AfrPunishmentInline(admin.TabularInline):
    model=AfrPunishment
    list_display = [ field.name for field in AfrPunishment._meta.fields]
    extra = 0
    


class PersonTagdedHistroyAdmin(admin.ModelAdmin):

    list_display = [ field.name for field in AfrTagdedHistroy._meta.fields]

class PersonTagdedHistroyInline(admin.TabularInline):

    model=AfrTagdedHistroy
    list_display = [ field.name for field in AfrTagdedHistroy._meta.fields]
    extra = 0

class PersonEffecincyAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in PersonEffecincy._meta.fields]
    search_fields = ['mil_ser__person_name','mil_ser__mil_ser','mil_ser__mil_no']

class PersonEffecincyInline(admin.TabularInline):
    model=PersonEffecincy
    list_display = [ field.name for field in PersonEffecincy._meta.fields]
    extra = 0

class PersonEffecincyL3YAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in PersonEffecincyL3Y._meta.fields]
    search_fields = ['mil_ser__person_name','mil_ser__mil_no','mil_ser__mil_ser']

class PersonEffecincyL3YInline(admin.TabularInline):
    model=PersonEffecincyL3Y
    list_display = [ field.name for field in PersonEffecincyL3Y._meta.fields]
    extra = 0

class PersonEffecincyAvgAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in PersonEffecincyAvg._meta.fields]
    search_fields = ['mil_ser__person_name','mil_ser__mil_no','mil_ser__mil_ser']

class PersonEffecincyAvgInline(admin.TabularInline):
    model=PersonEffecincyAvg
    list_display = [ field.name for field in PersonEffecincyAvg._meta.fields]
    extra = 0

class PunishmentStatisticsAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in PunishmentStatistics._meta.fields]
    readonly_fields = list_display
class PunishMentStatisticsInline(admin.TabularInline):
    model=PunishmentStatistics
    list_display = [ field.name for field in PunishmentStatistics._meta.fields]
    extra=0


class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in MedicalHistory._meta.fields]
    readonly_fields = list_display

class MedicalHistoryInline(admin.TabularInline):
    model=MedicalHistory
    list_display = [ field.name for field in MedicalHistory._meta.fields]
    extra = 0


class AfrEducationAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in AfrEducation._meta.fields]
    search_fields = ['mil_ser__mil_ser','mil_ser__mil_no','mil_ser__person_name']
    list_filter = ['mil_ser__degree_code','mil_ser__prnt_army_name','mil_ser__army_name']
    readonly_fields = list_display

class AfrEducationInline(admin.TabularInline):
    model = AfrEducation
    list_display = [ field.name for field in AfrEducation._meta.fields]
    extra=0



class AfrUnitsAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in AfrUnits._meta.fields]
    readonly_fields = list_display
    


class AfrUnitsInline(admin.TabularInline):
    model=AfrUnits
    list_display = [ field.name for field in AfrUnits._meta.fields]
    extra=0

class AfrTravelAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in AfrTravel._meta.fields]
    readonly_fields = list_display


class AfrTravelInline(admin.TabularInline):
    model=AfrTravel
    list_display = [ field.name for field in AfrTravel._meta.fields]
    readonly_fields = list_display
    extra= 0 

class AfrPsychologicalReportAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in AfrPsychologicalReport._meta.fields]
    search_fields = ['mil_ser__mil_ser','mil_ser__mil_no','mil_ser__person_name']
    list_filter  = ['mil_ser__degree_code','mil_ser__army_name','mil_ser__prnt_army_name','mil_ser__person_sex_name','active_flag']
    autocomplete_fields = ['mil_ser']

class AfrPsychologicalReportInline(admin.TabularInline):
    model = AfrPsychologicalReport
    list_display = [ field.name for field in AfrPsychologicalReport._meta.fields]
    extra = 0 


class AfrPersonAdmin(admin.ModelAdmin):

    list_display = [ field.name for field in AfrPerson._meta.fields]
    fields = [ field.name for field in AfrPerson._meta.fields]
    # readonly_fields = list_display
    search_fields = ['mil_ser','person_name','mil_no']
    list_filter = ['prnt_army_name','prnt_army_code','army_name','person_status_code','degree_code','person_sex_code']
    inlines = [
        AfrUnitsInline,
        FamilyInline,
        FamilyStatisticInline,
        AfrPunishmentInline,
        PunishMentStatisticsInline,
        PersonTagdedHistroyInline,
        PersonEffecincyInline,
        PersonEffecincyL3YInline,
        PersonEffecincyAvgInline,
        MedicalHistoryInline,
        AfrEducationInline,
        AfrVacationInline,
        PhotoInfoInline,
        AfrPhotoReportInline,
        LagnaPersonsInline,
        AfrTravelInline,
        AfrPsychologicalReportInline,
        AfrSecuritySituationInline,

        ]
    
    def get_queryset(self, request):
        return AfrPerson.all_objects.all()


admin.site.register(AfrPerson,AfrPersonAdmin)
admin.site.register(Family,FamilyAdmin)
admin.site.register(AfrPunishment,AfrPunishmentAdmin)
admin.site.register(AfrTagdedHistroy,PersonTagdedHistroyAdmin)
admin.site.register(PersonEffecincy,PersonEffecincyAdmin)
admin.site.register(PersonEffecincyL3Y,PersonEffecincyL3YAdmin)
admin.site.register(PersonEffecincyAvg,PersonEffecincyAvgAdmin)
admin.site.register(PunishmentStatistics,PunishmentStatisticsAdmin)
admin.site.register(MedicalHistory,MedicalHistoryAdmin)
admin.site.register(AfrEducation,AfrEducationAdmin)
admin.site.register(AfrUnits,AfrUnitsAdmin)
admin.site.register(FamilyStatistic,FamilyStatisticAdmin)
admin.site.register(AfrDegree,AfrDegreeAdmin)
admin.site.register(AfrTravel,AfrTravelAdmin)
admin.site.register(AfrPsychologicalReport,AfrPsychologicalReportAdmin)
admin.site.register(ArmyParentChild,ArmyPerentChildAdmin)
admin.site.register(AfrSecuritySituation,AfrSecuritySituationAdmin)
admin.site.register(MedicalLagnaResultLookUp,MedicalLagnaResultLookUpAdmin)
admin.site.register(AfrVacation,AfrVacationAdmin)