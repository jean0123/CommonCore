from import_export import resources

from .models import *

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UserDataResource(resources.ModelResource):
    class Meta:
        model = UserData

class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company