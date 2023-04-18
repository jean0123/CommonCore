# rest framework
from rest_framework.routers import DefaultRouter

# views
from .views import UserViewSet, UserDataViewSet, CompanyViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'user_data', UserDataViewSet, basename='user_data')
router.register(r'companies', CompanyViewSet, basename='companies')