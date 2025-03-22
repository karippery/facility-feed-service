
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "sex", "role",
            "is_verified", "is_staff", "is_superuser", "is_active",
            "created_date", "updated_date", "groups", "user_permissions"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
