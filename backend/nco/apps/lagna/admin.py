from django.contrib import admin
from django.utils.html import mark_safe,format_html
from apps.person.models import AfrPerson
from django.db.models import Exists,OuterRef
from .models import (
    LagnaPersons,
    LagnaPersonsOpinions,
    LagnaPersonVotes,
    OpinionType,
    LagnaType,
    LagnaCategory,
    LagnaVoteOpinoin,
    LagnaAfrStatus,
    VoteType,
    LagnaMemberType,
    LagnaMember,
    LagnaStatusType,
    LagnaTypeSpacific,
    LagnaPersonReasons,
    Lagna,
    LagnaAfrSnapData,
    LagnaCommSnapDetail,
    LagnaCommanderData,
    LagnaPersonPonsCons,
    PonsConsType,
    CommanderJobType,
    AfrSnapFinalDecition,
    AfrSnapOpinion,
)

# Register your models here.



def sort_by_degree(modeladmin,request,queryset):
    persons = queryset.filter(active_flag=True,delete_flag=False)
    counter = 1
    for person in persons:
        person.committe_order = counter
        person.save()
        counter += 1
    modeladmin.message_user(request,f'{persons.count()} items as updated')

def sort_by_order(modeladmin,request,queryset):
    persons = queryset.filter(active_flag=True,delete_flag=False).order_by('committe_order','mil_ser__army_code','mil_ser__person_sex_code','mil_ser__degree_code__degree_order','mil_ser__mil_no')
    counter = 1
    for person in persons:
        person.committe_order = counter
        person.save()
        counter += 1
    modeladmin.message_user(request,f'{persons.count()} items as updated')

def sort_by_femal_first(modeladmin,request,queryset):
    persons = queryset.filter(active_flag=True,delete_flag=False).order_by('-mil_ser__person_sex_code','mil_ser__army_code','mil_ser__degree_code__degree_order','mil_ser__mil_no')
    counter = 1
    for person in persons:
        person.committe_order = counter
        person.save()
        counter += 1
    modeladmin.message_user(request,f'{persons.count()} items as updated')

def sort_by_femal_first_order(modeladmin,request,queryset):
    persons = queryset.filter(active_flag=True,delete_flag=False).order_by('committe_order','-mil_ser__person_sex_code','mil_ser__army_code','mil_ser__degree_code__degree_order','mil_ser__mil_no')
    counter = 1
    for person in persons:
        person.committe_order = counter
        person.save()
        counter += 1
    modeladmin.message_user(request,f'{persons.count()} items as updated')

def set_final_decision_None(modeladmin,request,queryset):
    queryset.update(committe_decision=None)
    modeladmin.message_user(request,f'{queryset.count()} items as updated')


class VoteTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VoteType._meta.fields] 


class AfrSnapOpinionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AfrSnapOpinion._meta.fields] 
    search_fields = ['snap_id__mil_ser__mil_ser','snap_id__mil_ser__mil_no','snap_id__mil_ser__person_name']
    list_filter = ['snap_id__root_committe','snap_id__committe_type','snap_id__mil_ser__person_status_code','active_flag','opinion_type','opinion_code']
    autocomplete_fields = ['snap_id']

class AfrSnapOpinionInline(admin.TabularInline):
    model = AfrSnapOpinion
    list_display = [field.name for field in AfrSnapOpinion._meta.fields] 
    extra = 0
    

class AfrSnapFinalDecitionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AfrSnapFinalDecition._meta.fields] 
    autocomplete_fields = ['snap_id','committe_id']
    search_fields = ['snap_id__mil_ser__mil_no','snap_id__mil_ser__mil_ser','snap_id__mil_ser__person_name']

class AfrSnapFinalDecitionInline(admin.TabularInline):
    model = AfrSnapFinalDecition
    list_display = [field.name for field in AfrSnapFinalDecition._meta.fields] 
    extra = 0

class CommanderJobTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CommanderJobType._meta.fields] 

class LagnaPersonReasonsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaPersonReasons._meta.fields] 
    search_fields = ['snap_id__mil_ser__mil_ser','snap_id__mil_ser__mil_no']
    autocomplete_fields = ['snap_id']

    # + [ 'person_id__committe_type_code__committe_type__type_name']
    # search_fields = [ 'person_id__mil_ser__mil_no','person_id__mil_ser__person_name']
    # readonly_fields = list_display
    # exclude = ['reason_id']

class LagnaPersonReasonsInline(admin.TabularInline):
    model = LagnaPersonReasons
    list_display = [field.name for field in LagnaPersonReasons._meta.fields]
    # readonly_fields = list_display
    search_fields = [ 'person_id__mil_ser__mil_no','person_id__mil_ser__person_name']
    extra = 0


class LagnaPersonVotesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaPersonVotes._meta.fields]
    list_filter = ['active_flag','delete_flag','vote_member_id','person_id__committe_type_code']
    search_fields = ['person_id__mil_ser__mil_ser','person_id__mil_ser__mil_no','person_id__mil_ser__person_name']
    
class LagnaPersonVotesInline(admin.TabularInline):
    model = LagnaPersonVotes
    list_display = [field.name for field in LagnaPersonVotes._meta.fields]
    readonly_fields = list_display
    extra = 0


class LagnaPersonOpinionsAdmin(admin.ModelAdmin):
    list_display = ['person_id__committe_type_code__committe_code','person_id__committe_type_code'] + [field.name for field in LagnaPersonsOpinions._meta.fields]
    search_fields = ['person_id__mil_ser__mil_ser','person_id__mil_ser__mil_no','person_id__mil_ser__person_name']
    list_filter = ['active_flag','delete_flag','opinion_type','opinion_code','create_user']
    # autocomplete_fields = ['snap_id']

class LagnaPersonOpinionsInline(admin.TabularInline):
    model=LagnaPersonsOpinions
    list_display = [field.name for field in LagnaPersonsOpinions._meta.fields]
    extra = 0

class OpinionTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OpinionType._meta.fields] 
    list_editable = ['opinion_order']

class LagnaStatusTypeAdmin(admin.ModelAdmin):
    
    list_display = [field.name for field in LagnaStatusType._meta.fields]

#-------------------------- pons cons lookup --------------------------------------------------------
class PonsConsTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PonsConsType._meta.fields]

#-------------------------- lagna person cons and pons ----------------------------------------------
class LagnaPersonPonsConsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaPersonPonsCons._meta.fields]

class LagnaPersonPonsConsInline(admin.TabularInline):
    model = LagnaPersonPonsCons
    list_display = [field.name for field in LagnaPersonPonsCons._meta.fields]
    extra = 0
#-------------------------- Lagna commander snap details  --------------------------------------------------------

class LagnaCommSnapDetialAdmin(admin.ModelAdmin):
    model = LagnaCommSnapDetail
    list_display = [field.name for field in LagnaCommSnapDetail._meta.fields]
    inlines = [LagnaPersonOpinionsInline,LagnaPersonPonsConsInline]

class LagnaCommSnapDetialInline(admin.TabularInline):
    model = LagnaCommSnapDetail
    list_display = [field.name for field in LagnaCommSnapDetail._meta.fields]
    extra = 0

#-------------------------- Lagna commander  --------------------------------------------------------

class LagnaCommanderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaCommanderData._meta.fields]
    inlines = [  LagnaCommSnapDetialInline]

class LagnaCommanderInline(admin.TabularInline):
    model = LagnaCommanderData
    list_display = [field.name for field in LagnaCommanderData._meta.fields]
    extra = 0

#-------------------------- person snap data for lagna --------------------------------------

class LagnaAfrSnapDataAdmin(admin.ModelAdmin):

    list_display = [field.name for field in LagnaAfrSnapData._meta.fields]
    search_fields = ['mil_ser__person_name','mil_ser__mil_ser','mil_ser__mil_no']
    list_filter = ['root_committe','committe_type','active_flag','delete_flag']
    autocomplete_fields = ['mil_ser']
    inlines = [LagnaCommSnapDetialInline,AfrSnapFinalDecitionInline,AfrSnapOpinionInline]

    class Media:
        css = {
            "all":(r'admin/css/image_modal.css',)
        }
        js = (r'admin/js/image_modal.js',)

    def images_tag(self,obj):
        html=''
        for image in [obj.attach]:
            if image:
                # html +=f"<a href='{image.url}' target='_blank'><img src='{image.url}' style='height:150px; wigdth:150px;'/></a>"
                html +=f"""<div onclick="imagePopup('{image.url}')" onclick.self="clearImagePopup()"><img src='{image.url}' style='height:150px; wigdth:150px;'/></div>"""
        return format_html(html or '-')
    images_tag.short_description = "Images"

class LagnaAfrSnapDataInline(admin.TabularInline):
    model = LagnaAfrSnapData
    list_display = [field.name for field in LagnaAfrSnapData._meta.fields]
    extra = 0

#-------------------------- Lagna person  ----------------------------------------------------

class LagnaPersonsAdmin(admin.ModelAdmin):
    
    list_display = ['person_id','images_tag']+['mil_ser__mil_no','mil_ser__degree_code']+[field.name for field in LagnaPersons._meta.fields] + ['mil_ser__prnt_army_name']
    list_filter = ['committe_type_code__committe_type','committe_type_code__committe_code','mil_ser__prnt_army_name','mil_ser__army_name','mil_ser__degree_code','mil_ser__person_sex_name','active_flag','delete_flag','committe_decision','auth_nomination_flag']
    autocomplete_fields = ['mil_ser','committe_type_code']
    search_fields = ['mil_ser__person_name','mil_ser__mil_no','mil_ser__mil_ser','mil_ser__prnt_army_name','mil_ser__army_name']
    list_editable = ['committe_order']
    readonly_fields = ['images_tag']
    actions = [sort_by_degree,sort_by_order,sort_by_femal_first,sort_by_femal_first_order,set_final_decision_None]
    inlines = [LagnaPersonOpinionsInline,LagnaPersonVotesInline]

    class Media:
        css = {
            "all":(r'admin/css/image_modal.css',)
        }
        js = (r'admin/js/image_modal.js',)

    def get_queryset(self, request):
        return LagnaPersons.all_objects.all()

    def images_tag(self,obj):
        html=''
        for image in [obj.mil_ser.photos.filter(active_flag=True,delete_flag=False).first()]:
            if image:

                # html +=f"<a href='{image.photo_path.url}' target='_blank'><img src='{image.photo_path.url}' style='height:150px; wigdth:150px;'/></a>"
                html +=f"""<div onclick="imagePopup('{image.photo_path.url}')" onclick.self="clearImagePopup()"><img src='{image.photo_path.url}' style='height:150px; wigdth:150px;'/></div>"""
        return format_html(html or '-')
    images_tag.short_description = "Images"

class LagnaPersonsInline(admin.TabularInline):
    model = LagnaPersons
    list_display = [field.name for field in LagnaPersons._meta.fields] + ['mil_ser__prnt_army_name']
    autocomplete_fields = ['mil_ser']
    extra = 0

#----------------------- Lagna type lookup -----------------------------------------------------

class LagnaTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaType._meta.fields]

#---------------------- Member Type lookup -------------------------------------------------------
class LagnaMemberTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaMemberType._meta.fields]
    list_editable = ['socket_group']

class LagnaMemberTypeInline(admin.TabularInline):
    model = LagnaMemberType
    list_display = [field.name for field in LagnaMemberType._meta.fields]
    extra = 0

#---------------------- Members -------------------------------------------------------

class LagnaMemberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaMember._meta.fields]
    search_fields = ['member_user__username','member_user__first_name','member_user__first_name']
    list_filter = ['committe_code','active_flag']
    
class LagnaMemberInline(admin.TabularInline):
    model=LagnaMember
    list_display = [field.name for field in LagnaMember._meta.fields]
    extra = 0

# -------------------- Lagna Type Spacific -----------------------------------------

class LagnaTypeSpacificAdmin(admin.ModelAdmin):
    list_display = [ field.name for field in LagnaTypeSpacific._meta.fields ]
    search_fields = ['committe_code__committe_name']
    list_filter = ['committe_type']
    inlines = [LagnaPersonsInline]

class LagnaTypeSpacificInline(admin.TabularInline):
    model = LagnaTypeSpacific
    list_display = [ field.name for field in LagnaTypeSpacific._meta.fields ]
    # readonly_fields = list_display
    extra = 0


class LagnaVoteOpinionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaVoteOpinoin._meta.fields]
    list_filter = ['committe_type_code']

class LagnaStatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LagnaAfrStatus._meta.fields]

    
class LagnaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Lagna._meta.fields]
    list_filter = ['main_committe_code','committe_category','active_flag']
    search_fields = ['committe_name']
    inlines= [LagnaTypeSpacificInline,LagnaMemberInline]

class LagnaInline(admin.TabularInline):
    model=Lagna
    list_display = [field.name for field in Lagna._meta.fields]
    extra = 0
    

class LagnaCategoryAdmin(admin.ModelAdmin):
    
    list_display = [field.name for field in LagnaCategory._meta.fields]
    inlines =  [LagnaInline]
    

class LagnaCategorInline(admin.TabularInline):
    
    model=LagnaCategory
    list_display = [field.name for field in LagnaCategory._meta.fields]
    extra=0

admin.site.register(LagnaPersons,LagnaPersonsAdmin)
admin.site.register(LagnaType,LagnaTypeAdmin)
admin.site.register(LagnaVoteOpinoin,LagnaVoteOpinionAdmin)
admin.site.register(LagnaAfrStatus,LagnaStatusAdmin)
admin.site.register(Lagna,LagnaAdmin)
admin.site.register(LagnaMemberType,LagnaMemberTypeAdmin)
admin.site.register(LagnaMember,LagnaMemberAdmin)
admin.site.register(LagnaCategory,LagnaCategoryAdmin)
admin.site.register(LagnaStatusType,LagnaStatusTypeAdmin)
admin.site.register(LagnaTypeSpacific,LagnaTypeSpacificAdmin)
admin.site.register(OpinionType,OpinionTypeAdmin)
admin.site.register(LagnaPersonsOpinions,LagnaPersonOpinionsAdmin)
admin.site.register(LagnaPersonVotes,LagnaPersonVotesAdmin)
admin.site.register(LagnaPersonReasons,LagnaPersonReasonsAdmin)
admin.site.register(LagnaAfrSnapData,LagnaAfrSnapDataAdmin)
admin.site.register(PonsConsType,PonsConsTypeAdmin)
admin.site.register(LagnaPersonPonsCons,LagnaPersonPonsConsAdmin)
admin.site.register(LagnaCommanderData,LagnaCommanderAdmin)
admin.site.register(LagnaCommSnapDetail,LagnaCommSnapDetialAdmin)
admin.site.register(CommanderJobType,CommanderJobTypeAdmin)
admin.site.register(AfrSnapFinalDecition,AfrSnapFinalDecitionAdmin)
admin.site.register(AfrSnapOpinion,AfrSnapOpinionAdmin)
admin.site.register(VoteType,VoteTypeAdmin)