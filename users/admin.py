from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from .resources import *
from .models import *

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = UserResource
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    data_hierarchy = 'created'
    search_fields = ('username', 'first_name', 'last_name')

@admin.register(UserData)
class UserDataAdmin(ImportExportModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    
    data_hierarchy = 'created'
    search_fields = ('user__username', 'phone', 'company__name')
    resource_class = UserDataResource

@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    
    data_hierarchy = 'created'
    search_fields = ('name', 'phone', 'email', 'contact_person')
    resource_class = CompanyResource
