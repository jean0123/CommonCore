from django.db import models
from utilities.core_file import CoreModel
from users.models import User
from simple_history.models import HistoricalRecords


class ListType(CoreModel):
    parent = models.ForeignKey('lists.ListType', on_delete=models.CASCADE, related_name='parent_list',
                               null=True, blank=True, verbose_name='Parent list type')
    code = models.CharField(max_length=100, verbose_name='Code', blank=True, null=True)
    name = models.CharField(max_length=150, verbose_name='Name', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    name_en = models.CharField(max_length=150, verbose_name='Name_en', blank=True, null=True)
    description_en = models.TextField(verbose_name='Description_en', blank=True, null=True)
    name_pt = models.CharField(max_length=150, verbose_name='Name_pt', blank=True, null=True)
    description_pt = models.TextField(verbose_name='Description_pt', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'List type'
        verbose_name_plural = 'Types of lists'
        ordering = ['name']

class ListItem(CoreModel):
    parent = models.ForeignKey('lists.ListItem', on_delete=models.CASCADE,
                               null=True, blank=True, verbose_name='Parent item')
    list_type = models.ForeignKey(ListType, on_delete=models.CASCADE,
                                  null=False, blank=False, verbose_name='List item')
    code = models.CharField(max_length=100, verbose_name='Code', blank=True, null=True)
    name = models.CharField(max_length=150, verbose_name='Name', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    name_en = models.CharField(max_length=150, verbose_name='Name_en', blank=True, null=True)
    description_en = models.TextField(verbose_name='Description_en', blank=True, null=True)
    name_pt = models.CharField(max_length=150, verbose_name='Name_pt', blank=True, null=True)
    description_pt = models.TextField(verbose_name='Description_pt', blank=True, null=True)

    def __str__(self):
        return self.list_type.name + ' - ' + self.name

    class Meta:
        verbose_name = 'List item'
        verbose_name_plural = 'List items'
        ordering = ['name']

class State(CoreModel):
    """Model definition for State."""
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    historical = HistoricalRecords()

    class Meta:
        """Meta definition for State."""
        verbose_name = 'State'
        verbose_name_plural = 'States'
        ordering = ['-created']
    
    def __str__(self):
        """Unicode representation of State."""
        return self.name

class Notification(CoreModel):
    """Model definition for Notification."""
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_notification')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_notification')
    url = models.CharField(max_length=100, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='state_notification')
    historical = HistoricalRecords()

    class Meta:
        """Meta definition for Notification."""
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created']
    
    def __str__(self):
        """Unicode representation of Notification."""
        return self.title