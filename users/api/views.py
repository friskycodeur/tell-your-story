from .serializers import UserSerializer
from users.models import User
from .serializers import ModeratorRegisterSerializer, MemberRegisterSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.backends import TokenBackend
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from django.core.exceptions import ValidationError


def get_tokens_for_user(user):

    """
    Returns the refresh and access token for user.
    """

    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_user_from_token(request):

    """
    Returns the user from access token.
    """

    token = request.META.get("HTTP_AUTHORIZATION", " ").split(" ")[1]
    data = {"token": token}
    try:
        valid_data = TokenBackend(algorithm="HS256").decode(
            token, verify=False
        )
        user = valid_data["user"]
        request.user = user
    except ValidationError as v:
        print("validation error", v)


class ModeratorRegisterAPIView(generics.CreateAPIView):

    """
    Handles Moderator Registration.
    """

    queryset = User.objects.all()
    serializer_class = ModeratorRegisterSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class MemberRegisterAPIView(generics.CreateAPIView):

    """
    Handles Member Registration.
    """

    queryset = User.objects.all()
    serializer_class = MemberRegisterSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class MemberList(generics.ListAPIView):

    """
    Returns Member list.
    """

    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(account_type="Member")


class ModeratorList(generics.ListAPIView):

    """
    A view that returns Moderator list.
    """

    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(account_type="Moderator")


class UserDetail(generics.RetrieveAPIView):

    """
    A view that returns user details from username.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, username):
        queryset = User.objects.filter(username=username)
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(["POST"])
def login(request):

    """
    A view that handles login for buyers and nurseries.
    """

    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response(
            {"error": "Please provide both username and password"},
            status=HTTP_400_BAD_REQUEST,
        )
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"error": "Invalid Credentials"}, status=HTTP_404_NOT_FOUND
        )
    token = get_tokens_for_user(user)
    serializer = UserSerializer(user)
    data = serializer.data
    return Response({"data": data}, status=HTTP_200_OK)
