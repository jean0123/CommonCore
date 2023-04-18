# django
from django.db import models
from django.contrib.auth.models import AbstractUser

# utilities
from utilities.core_file import CoreModel
from simple_history.models import HistoricalRecords

class User(CoreModel, AbstractUser):
    """User model
    Extend from Django's Abstract User, change the username field to email.
    """
    historical = HistoricalRecords()
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created']

class UserData(CoreModel):
    """User data model
    Profile data for each user in the system.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_data'
    )
    company = models.ForeignKey(
        'users.Company',
        on_delete=models.CASCADE,
        related_name='user_company',
        null=True,
        blank=True
    )
    company_role = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='cargados/users/avatars/', blank=True, null=True)
    adress = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=3, blank=True, null=True, default='en')
    employee_id = models.CharField(max_length=255, blank=True, null=True)
    historical = HistoricalRecords()

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'User data'
        verbose_name_plural = 'Users data'
        ordering = ['-created']

class Company(CoreModel):
    """Company model
    Model for companies that have users in the platform.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='users/logos/', blank=True, null=True)
    email = models.EmailField(
        'email address',
        unique=False,
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    contact_person = models.CharField(max_length=255,null=True, blank=True)
    contact_person_email = models.EmailField(
        'email address',
        unique=False,
        null=True,
        blank=True
    )
    contact_person_phone = models.CharField(max_length=255, null=True, blank=True)
    contact_person_position = models.CharField(max_length=255, null=True, blank=True)
    historical = HistoricalRecords()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created']
