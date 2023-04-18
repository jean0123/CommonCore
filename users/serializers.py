"""Serializers for the Users app."""

# django
import os
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

# rest_framework
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# models
from users.models import User, UserData, Company
from core.core_file import CoreSerializer

def validar_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class PermissionSerializer(CoreSerializer):
    """Permission serializer."""

    class Meta:
        """Meta class."""
        model = Permission
        fields = '__all__'

class GroupSerializer(CoreSerializer):
    """Group serializer."""
    permissions_code = serializers.StringRelatedField(many=True, read_only=True, source='permissions')

    class Meta:
        """Meta class."""
        model = Group
        fields = '__all__'

class UserSerializer(CoreSerializer):
    """User serializer."""
    permissions_code = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)

    def get_permissions_code(self, obj):
        """Get permissions code."""
        if obj.is_superuser:
            permiss = User(is_superuser=True).get_all_permissions()
            return permiss
        else:
            permiss = Permission.objects.filter(group__user=obj)
            return permiss.values_list('codename', flat=True)

    def get_user_data(self, obj):
        """Get user data."""
        try:
            data = UserData.objects.get(user=obj, is_active_status=True)
            return UserDataSerializer(data).data
        except:
            return None
    
    def create(self, validated_data):
        """Create user."""
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user

    class Meta:
        """Meta class."""
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'groups',
            'user_data',
            'permissions_code',
            'user_permissions',
        ]

class UserSerializerShort(CoreSerializer):
    """User serializer short."""
    class Meta:
        """Meta class."""
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
        ]

class UserSingUpSerializer(CoreSerializer):
    """User sing up serializer."""
    username = serializers.CharField(min_length=6, max_length=64, required=True)
    password = serializers.CharField(min_length=8, max_length=64, required=True)
    email = serializers.EmailField(required=False)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    first_name = serializers.CharField(min_length=2, max_length=64, required=False)
    last_name = serializers.CharField(min_length=2, max_length=64, required=False)
    is_active = serializers.BooleanField(default=True)
    is_superuser = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)

    def validate(self, data):
        """Verify password match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Passwords do not match.')
        return data
    
    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user
    
    class Meta:
        """Meta class."""
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirmation',
            'first_name',
            'last_name',
            'is_active',
            'is_superuser',
            'is_staff',
        ]

class CargarSerializer(serializers.Serializer):
    archivo = serializers.FileField(validators=[validar_extension])

class UserDataSerializer(CoreSerializer):
    """User data serializer."""

    class Meta:
        """Meta class."""

        model = UserData
        fields = '__all__'

class CompanySerializer(CoreSerializer):
    """Company serializer."""

    class Meta:
        """Meta class."""

        model = Company
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """My token obtain pair serializer."""

    @classmethod
    def get_token(cls, user):
        """Get token."""
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_active'] = user.is_active
        token['groups'] = user.groups.values_list('name', flat=True)
        token['user_permissions'] = user.get_all_permissions()
        token['user_data'] = UserDataSerializer(UserData.objects.get(user=user, is_active_status=True)).data

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
