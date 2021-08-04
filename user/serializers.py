from rest_framework import serializers

from user.models import User, APIKey


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']


class UserAPIKeySerializers(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__'


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
