from django.urls import path
from users.views import UserDetailView, UserListCreateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("", UserListCreateView.as_view(), name="user-list-create"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
