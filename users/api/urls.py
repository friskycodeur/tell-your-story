from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from .views import (
    ModeratorRegisterAPIView,
    MemberRegisterAPIView,
    MemberList,
    UserDetail,
    ModeratorList,
    login,
)
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("register/moderator/", ModeratorRegisterAPIView.as_view()),
    path("register/member/", MemberRegisterAPIView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("members/", MemberList.as_view()),
    path("moderators/", ModeratorList.as_view()),
    path("users/<username>", UserDetail.as_view()),
    path("login/", login),
]
