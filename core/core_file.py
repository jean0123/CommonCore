from django.db import models
from django.conf import settings
from safedelete.models import SOFT_DELETE_CASCADE
from rest_flex_fields import FlexFieldsModelSerializer

class CoreModel(models.Model):
    _safedelete_policy = SOFT_DELETE_CASCADE
    is_active_status = models.BooleanField(default=True, blank=True, verbose_name='Active')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Updated at', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+',
                                   blank=True, null=True, verbose_name="Created by", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+',
                                   blank=True, null=True, verbose_name="Modificated by", on_delete=models.PROTECT)

    def active(self):
        self.is_active = True
        self.save()

    def deactive(self):
        self.is_active = False
        self.save()
    
    class Meta:
        abstract = True
        get_latest_by = 'created'

class CoreSerializer(FlexFieldsModelSerializer):

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(CoreSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super(CoreSerializer, self).update(instance, validated_data)