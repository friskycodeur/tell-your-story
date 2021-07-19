from rest_framework import request, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListAPIView,
)
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Story, Upvote, Comment
from .serializers import (
    StoryAddSerializer,
    StoryDetailSerializer,
    StoryUpdateSerializer,
    StoryListSerializer,
)


class StoryAddView(CreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryAddSerializer
    permission_classes = (IsAuthenticated,)


class StoryDeleteView(DestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryDetailSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)


class StoryDetailView(RetrieveAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryDetailSerializer
    lookup_field = "id"
    permission_classes = (AllowAny,)


class StoryUpdateView(UpdateAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryUpdateSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)


class StoryListView(ListAPIView):
    serializer_class = StoryListSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    permission_classes = (AllowAny,)
