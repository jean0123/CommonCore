from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from .models import *
from .serializers import *

class ListItemViewSet(viewsets.ModelViewSet):
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'name_en', 'name_pt')
    filterset_fields = ('is_active_status', )
    permission_classes = []
        
class ListItemViewPadreSet(viewsets.ModelViewSet):
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'name_en', 'name_pt')
    filterset_fields = ('is_active_status', )
    pagination_class = None
    permission_classes = ()

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        parent = self.kwargs.get('parent', None)
        return self.queryset.filter(list_type_id=pk, parent_id=parent)

class ListItemFiltroViewSet(viewsets.ModelViewSet):
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'name_en', 'name_pt')
    filterset_fields = ('is_active_status', )
    permission_classes = []
    pagination_class = None

    def get_queryset(self):
        if (self.request.GET.get('parent')):
            pa = self.request.GET.get('parent')
            queryset = self.queryset.filter(parent_id=pa)
            return queryset
        else:
            tipo = self.request.GET.get('type')
            queryset = self.queryset.filter(list_type__codigo=tipo)
            return queryset

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', )
    filterset_fields = ('is_active_status', )
    permission_classes = []

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('from_user__username', 'to_user__username', 'state__name')
    filterset_fields = ('is_active_status', )
    permission_classes = []

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        state = State.objects.get_or_create(name=request.data['state'])[0]
        data['state'] = state.id
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)