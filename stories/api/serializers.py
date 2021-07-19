from django.conf import settings
from ..models import Story, Comment, Upvote
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from authentication.serializers import UserSerializer


User = settings.AUTH_USER_MODEL


class StoryAddSerializer(ModelSerializer):
    class Meta:
        model = Story
        exclude = (
            "id",
            "slug",
        )


class StoryDetailSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="story-api:story-detail", lookup_field="id"
    )
    user = UserSerializer(read_only=True)
    html = SerializerMethodField()
    comments = SerializerMethodField()
    upvotes = SerializerMethodField()

    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "content",
            "content",
            "html",
            "publish",
            "created_by",
            "created_at",
            "updated_at",
            "comments",
            "likes",
            "is_anonymous",
            "disable_comments",
            "is_visible",
        ]

    def get_html(self, obj):
        return obj.get_markdown()

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

    def get_likes(self, obj):
        c_qs = Like.objects.filter_by_instance(obj)
        comments = LikeListSerializer(c_qs, many=True).data
        return comments
