from django.urls import path
from .views import RegisterView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('/api/auth/register/',RegisterView.as_view(),name='aut_register'),
    path('api/auth/token', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/user/', UserDetailView.as_view(), name='user_details'),
]