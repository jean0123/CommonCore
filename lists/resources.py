from import_export import resources

from .models import *

class ListTypeAdminResource(resources.ModelResource):
    class Meta:
        model = ListType

class ListItemAdminResource(resources.ModelResource):
    class Meta:
        model = ListItem

class StateAdminResource(resources.ModelResource):
    class Meta:
        model = State

class NotificationAdminResource(resources.ModelResource):
    class Meta:
        model = Notification

