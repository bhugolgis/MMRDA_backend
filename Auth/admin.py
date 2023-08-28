
# Register your models here.

from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User
    list_display = ('email', 'username' ,'is_staff','is_active',)
    list_filter = ('email', 'username','is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active' , 'is_mmrda' , 'is_kfw' , 'is_consultant' , 'is_contractor' ,'groups' , 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

# admin.site.register(report)
# admin.site.register(GroupManager)
# # #admin.site.register(project_issue)
# # admin.site.register(traning)
# # # admin.site.register(occupationalHealthSafety)
# admin.site.register(photographs)
class OutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True 
    
    def get_actions(self, request):
        actions = super(OutstandingTokenAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)