from rest_framework.permissions import  BasePermission
from django.contrib.auth.models import Group


def _is_in_group(user, group_name):
    """
    This function takes user and group as parameter and returns true if the user is present in that group
    """

    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist as e:
        return None


def _has_group_permission(user, required_group):
    """
    This function takes the user and checks if the user is in the list of group
    """
    return any([_is_in_group(user, group_name) for group_name in required_group])


class IsConsultant(BasePermission):
    required_group = ["consultant"]
    """
    The function checks if the user has the required group permission.

    """

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_group)
        return request.user and has_group_permission


class IsContractor(BasePermission):
    required_group = ["contractor"]

    def has_permission(self, request, view):
        """
        The function checks if the user has a specific group permission.
        
        """
        has_group_permission = _has_group_permission(
            request.user, self.required_group)
        return request.user and has_group_permission

class IsRNR(BasePermission):
    required_group = ["RNR"]

    def has_permission(self, request, view):
        """
        The function checks if the user has a specific group permission.
        
        """
        has_group_permission = _has_group_permission(
            request.user, self.required_group)
        return request.user and has_group_permission



# class CustomModelPermissions(DjangoModelPermissions):
#     perms_map = {
#         'GET': ['%(app_label)s.view_%(model_name)s'],
#         'OPTIONS': [],
#         'HEAD': [],
#         'POST': ['%(app_label)s.add_%(model_name)s'],
#         'PUT': ['%(app_label)s.change_%(model_name)s'],
#         'PATCH': ['%(app_label)s.change_%(model_name)s'],
#         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
#     }

