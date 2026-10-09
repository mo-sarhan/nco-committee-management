from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadAnyWriteStaff(BasePermission):
    """everybody logged in can read the layout, only staff can change it"""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_staff
            or request.user.is_superuser
            or request.user.has_perm('uisettings.can_manage_ui_settings')
        )
