from rest_framework import serializers

from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):

    """
    Serializes user data - username, email, token
    """

    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = (
            "first_name",
            "last_name",
            "password",
            "user_permissions",
            "groups",
            "is_staff",
            "is_superuser",
            "last_login",
        )

    def get_token(self, value):
        refresh = RefreshToken.for_user(value)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserAPISerializer(serializers.ModelSerializer):

    """
    Serializes User data - username, verified, email
    """

    class Meta:
        model = User
        fields = ["username", "verified", "email"]


class ModeratorRegisterSerializer(serializers.ModelSerializer):

    """
    Serializes Moderator Registration data
    """

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    account_type = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    verified = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "account_type",
            "message",
            "verified",
            "token",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_message(self, obj):
        return "Thank you for registering, fellow moderator."

    def get_account_type(self, obj):
        return "Moderator"

    def get_verified(self, obj):
        return False

    def get_token(self, value):
        refresh = RefreshToken.for_user(value)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this email already exists"
            )
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this username already exists"
            )
        return value

    def validate(self, data):
        pw = data.get("password")
        pw2 = data.pop("password2")
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User.objects.create(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            account_type="Moderator",
            verified=False,
        )
        user_obj.set_password(validated_data.get("password"))
        user_obj.save()
        return user_obj


class MemberRegisterSerializer(serializers.ModelSerializer):

    """
    Serializes Member Registration data
    """

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    message = serializers.SerializerMethodField(read_only=True)
    account_type = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    verified = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "message",
            "account_type",
            "verified",
            "token",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_message(self, obj):
        return "Thank you for registering. You can now log in to and start reading !"

    def get_account_type(self, obj):
        return "Member"

    def get_verified(self, obj):
        return False

    def get_token(self, value):
        refresh = RefreshToken.for_user(value)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this email already exists"
            )
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(
                "User with this username already exists"
            )
        return value

    def validate(self, data):
        pw = data.get("password")
        pw2 = data.pop("password2")
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User.objects.create(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            account_type="Member",
            verified=False,
        )
        user_obj.set_password(validated_data.get("password"))
        user_obj.save()
        return user_obj
