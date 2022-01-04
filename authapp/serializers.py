from djoser.serializers import UserCreateSerializer

from .models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'address',
                  'city', 'zip_code', 'house_img')


