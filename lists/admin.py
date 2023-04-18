from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ListType, ListItem
from .resources import *

@admin.register(ListType)
class ListTypeAdmin(ImportExportModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    
    search_fields = ('name', 'code')
    list_filter = ('parent__name',)
    resource_class = ListTypeAdminResource

@admin.register(ListItem)
class ListItemAdmin(ImportExportModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    search_fields = ('id', 'name', 'code', 'parent__name')
    list_filter = ('list_type__name', 'is_active_status')
    resource_class = ListItemAdminResource

@admin.register(State)
class StateAdmin(ImportExportModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    search_fields = ('name', )
    resource_class = StateAdminResource

@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    search_fields = ('from_user__username', 'to_user__username')
    resource_class = NotificationAdminResource

