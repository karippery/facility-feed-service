
from facility_feed_service.utils.paginations import DefaultPagination
from users.models import User
from users.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["email", "first_name", "last_name"]
    pagination_class = DefaultPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, request):
        user = serializer.save()
        password = request.data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return user


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.only("id", "email", "first_name", "last_name")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer, password=None):
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        password = request.data.get("password")
        self.perform_update(serializer, password=password)
        return Response(serializer.data, status=status.HTTP_200_OK)
