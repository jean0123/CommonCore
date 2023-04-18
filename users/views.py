# rest framework
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.decorators import action
from django.contrib.auth.models import Group

# models
from .models import User, UserData, Company
from utilities.utilities import UsuariosBulk

# serializers
from .serializers import (
    UserDataSerializer,
    UserSerializer,
    CompanySerializer,
    CustomTokenObtainPairSerializer,
    CargarSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.prefetch_related(
        'user_data',
        'groups',
        'groups__permissions',
        'user_permissions',
        'user_permissions__content_type',
        'user_permissions__content_type__app_label',
        'user_permissions__content_type__model',
    ).filter(
        is_active_status=True,
        is_active=True
    ).exclude(
        username='jean'
    )
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filterset_fields = ['is_active_status', ]

    def get_queryset(self):
        company = self.request.query_params.get('company', None)
        group = self.request.query_params.get('group', None)
        if company:
            return self.queryset.filter(user_data__company__id=company)
        if group:
            return self.queryset.filter(groups__name=group)
        return self.queryset

    @action(detail=False, methods=['post'])
    def signup_bulk(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = CargarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            base_limpia = (
                UsuariosBulk(
                    request.FILES.get('archivo'),
                )
                    .transformar()
            )
        except Exception as e:
            message = _("Error to read the file.")
            return Response({
                'status': 'error',
                'message': message,
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        errores = []
        usuarios = []
        with transaction.atomic():
            contador = 0
            for usuario in base_limpia:
                company = Company.objects.get(name=usuario['compania'], is_active_status=True)
                group = Group.objects.get(name=usuario['role'])
                try:
                    user = User.objects.get(username__iexact=usuario['username'], is_active_status=True)
                except:
                    try:
                        user = User.objects.create_user(
                            username=usuario['username'],
                            email=usuario['email'],
                            first_name=usuario['first_name'],
                            last_name=usuario['last_name'],
                            password=usuario['password'] if usuario['password'] else 'Humand2023!',
                        )
                        user.groups.add(group)
                        user.save()
                        usuarios.append(user)
                        contador += 1
                    except Exception as e:
                        errores.append({
                            'username': usuario['username'],
                            'error': str(e)
                        })
                else:
                    user.set_password(usuario['password'] if usuario['password'] else 'Humand2023!')
                    user.save()
                    errores.append({
                        'username': usuario['username'],
                        'error': 'The user already exists. password updated.'
                    })
                try:
                    userdata = UserData.objects.get(user=user, is_active_status=True)
                except:
                    try:
                        UserData.objects.create(
                            user=user,
                            company=company
                        )
                    except Exception as e:
                        errores.append({
                            'username': usuario['username'],
                            'error': str(e)
                        })
                else:
                    userdata.company = company
                    userdata.save()
        if len(errores) > 0:
            message = _("Some users could not be created.")
            return Response({
                'status': 'warning',
                'message': message,
                'usuarios_creados': contador,
                'errores': errores
            }, status=status.HTTP_201_CREATED)
        else:
            message = _("Users created successfully.")
            return Response({
                'status': 'success',
                'message': message,
            }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def get_language(self, request, *args, **kwargs):
        user = request.user
        userData = UserData.objects.get(user=user, is_active_status=True)
        message = _("Language get successfully.")
        return Response({
            'status': 'success',
            'message': message,
            'data': userData.language
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def update_language(self, request, *args, **kwargs):
        data = request.data.copy()
        user = request.user
        userData = UserData.objects.get(user=user, is_active_status=True)
        userData.language = data['language']
        userData.save()
        message = _("Language updated successfully.")
        return Response({
            'status': 'success',
            'message': message,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def upload_avatar(self, request, *args, **kwargs):
        data = request.data.copy()
        user = request.user
        userData = UserData.objects.get(user=user, is_active_status=True)
        if data['avatar']:
            userData.avatar = data['avatar']
            userData.save()
            message = _("Avatar updated successfully.")
            return Response({
                'status': 'success',
                'message': message,
            }, status=status.HTTP_200_OK)
        else:
            message = _("Avatar not updated.")
            return Response({
                'status': 'error',
                'message': message,
            }, status=status.HTTP_400_BAD_REQUEST)

class UserDataViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user data instances.
    """
    queryset = UserData.objects.none()
    serializer_class = UserDataSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_queryset(self):
        return UserData.objects.filter(user=self.request.user, is_active_status=True)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = UserDataSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing company instances.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'phone']

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # get the user
        user = User.objects.filter(
            username__iexact=request.data['username'],
            is_active_status=True).first()
        if not user:
            message = _("The user does not exist.")
            return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)
        # authenticate the user
        user = authenticate(username=user.username, password=request.data['password'])
        if user is not None:
            # create the token
            refresh = RefreshToken.for_user(user)
            # serialize the user
            serializer = UserSerializer(user).data
            # return the response
            message = _("Logged in successfully.")
            return Response({
                'detail': message,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer
            }, status=status.HTTP_200_OK)
        else:
            message = _("Invalid Credentials.")
            return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)

class Logout(GenericAPIView):

    def post(self, request, *args, **kwargs):
        # blacklist the refresh token
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            message = _("Successfully logged out.")
            return Response({'detail': message}, status=status.HTTP_205_RESET_CONTENT)
        except:
            message = _("Invalid token.")
            return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)
