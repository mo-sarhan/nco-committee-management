from rest_framework.permissions import BasePermission
from django.utils import timezone
from django.contrib.auth.models import User

class HasPermToRejectPhoto(BasePermission):

    def has_permission(self, request, view):
        # print('hererere'*5)
        if request.user.is_superuser:
            return True
        if request.user.has_perms(['photos.can_reject_photo']):
            return True


        return False
