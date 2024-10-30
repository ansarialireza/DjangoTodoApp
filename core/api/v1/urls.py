from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

app_name = 'v1'

urlpatterns = [
    path('', include(router.urls)),   

    path('authentication/token/', obtain_auth_token, name='obtain_auth_token'),
    path('authentication/jwt-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authentication/jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]