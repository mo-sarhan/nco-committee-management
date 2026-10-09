from django.contrib import admin
from django.utils.html import mark_safe,format_html_join

from .models import (
    PrntPhotoReport,
    UnitPhotoReport,
    AfrPhotoReport,
    LagnaAfrReport,
    LagnaAfrOpinionsReport,

)
# Register your models here.



#-------------------------------------- photo report ------------------------------------------------------------------
class PrntPhotoReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PrntPhotoReport._meta.fields]
    readonly_fields = list_display
class UnitPhotoReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UnitPhotoReport._meta.fields]
    readonly_fields = list_display
    search_fields = ['unit_name','unit_code','prnt_army_name','prnt_army_code']
    list_filter = ['prnt_army_name','completed','un_completed','checked','un_checked','approved','not_approved','rest']
    
class AfrPhotoReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AfrPhotoReport._meta.fields] + ['images_tag']
    readonly_fields = list_display
    list_filter = ['completed_flag','checked_flag','approved_flag','active_flag','delete_flag','lock_half','lock_tall','lock_family','mil_ser__prnt_army_name','mil_ser__person_sex_name']
    search_fields = ['mil_ser__mil_ser','mil_ser__mil_no','mil_ser__person_name']

    def images_tag(self,obj):
        html=''
        photos = obj.mil_ser.photos.filter(active_flag=True,delete_flag=False)
        if not photos:
            return '-'
        html_format ="<a href='{0}' target='_blank'><img src='{0}' style='height:150px; wigdth:150px;'/></a>"
        return format_html_join(html ,html_format,((photo.photo_path.url,) for photo in photos))
    images_tag.short_description = "Images"


class AfrPhotoReportInline(admin.TabularInline):
    model = AfrPhotoReport
    list_display = [field.name for field in AfrPhotoReport._meta.fields]
    readonly_fields = list_display
    extra = 0


admin.site.register(PrntPhotoReport,PrntPhotoReportAdmin)
admin.site.register(UnitPhotoReport,UnitPhotoReportAdmin)
admin.site.register(AfrPhotoReport,AfrPhotoReportAdmin)


#----------------- lagna report -------------------------------------------

class LagnaAfrReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaAfrReport._meta.fields]
    readonly_fields = list_display
    list_filter = ['prnt_army_name','type_name','person_prnt_army_name']

class LagnaAfrOpinionsReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaAfrOpinionsReport._meta.fields]
    readonly_fields = list_display
    list_filter = ['committe_code','spacific_code','spacific_code__committe_type','army_code','prnt_army_code','opinion_code','vote_code']


admin.site.register(LagnaAfrReport,LagnaAfrReportAdmin)
admin.site.register(LagnaAfrOpinionsReport,LagnaAfrOpinionsReportAdmin)