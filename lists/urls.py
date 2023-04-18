# rest framework
from rest_framework.routers import DefaultRouter

# views
from .views import *

router = DefaultRouter()

router.register(r'list_item', ListItemViewSet, basename='list_item')
router.register(r'list_item_padre', ListItemViewPadreSet, basename='list_item_padre')
router.register(r'list_item_filtro', ListItemFiltroViewSet, basename='list_item_filtro')
router.register(r'state', StateViewSet, basename='state')
router.register(r'notification', NotificationViewSet, basename='notification')