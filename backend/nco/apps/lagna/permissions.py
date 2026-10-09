from rest_framework.permissions import BasePermission
from django.utils import timezone
from django.contrib.auth.models import User


class IsOwnerOrSuperUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.committe_create_user == request.user
    def has_permission(self, request, view):
        if request.user.has_perms(['lagna.add_lagna','lagna.change_lagna','lagna.delete_lagna']):
            return True


        return False




class AllowToAddOrEditPerson(BasePermission):
    # def has_object_permission(self, request, view, obj):

    #     if request.user.is_superuser:
    #         return True
    #     if obj.committe_type_code.end_date > timezone.now():
    #         if hasattr(request.user,'profile'):
    #             if request.user.profile.prnt_army_code in [obj.mil_ser.prnt_army_code , obj.mil_ser.army_code]:
    #                 # if request.user.has_perms(['lagna.add_lagnaperson','lagna.change_lagnaperson']):
    #                     return True
    #     return False
    def has_permission(self, request, view):
            return True
            # if request.user.is_superuser:
            #     return True
            # print('super',request.user.is_superuser)
            # # if request.user.has_module_perms('lagna'):
            # #     return True
            # # if request.user.has_perms({'lagna.add_lagnapersons', 'lagna.change_lagnapersons','lagna.delete_lagnapersons'}):
            # return True
            # return False

class AllowToVote(BasePermission):
    def has_permission(self, request, view):
            if request.user.is_superuser:
                return True
            # print('super',request.user.is_superuser)
            # if request.user.has_module_perms('lagna'):
            #     return True
            if request.user.has_perm('lagna.add_lagnapersonvotes'):
                return True
            return False

class AllowToSetOpinion(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.committe_type_code.end_date > timezone.now():
            if obj.committe_status_code_id < 20: 
                if ((obj.mil_ser.prnt_army_code == request.user.profile.prnt_army_code) or (obj.mil_ser.army_code == request.user.profile.prnt_army_code)) and request.user.has_perms({'opiniontype.can_set_opinion'}):
                    return True
        return False
    def has_permission(self, request, view):
            if request.user.is_superuser:
                return True
            if request.user.has_perms({'opiniontype.can_set_opinion'}):
                return True
            return False


            

class AllowToSetReview(BasePermission):
     def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.has_perm('lagna.can_set_review'):
            return True
        # print(request.user.has_perm('lagna.can_set_review'))
        # print(request.user.get_all_permissions())
        return False

class AllowToSetConf(BasePermission):
     def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.has_perm('lagna.can_set_conf'):
            return True
        return False

class AllowToSetWaitingDate(BasePermission):
     def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.has_perm('lagna.can_set_waiting_date'):
            return True
        return False