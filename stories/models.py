from django.db import models
from django.conf import settings
from base.models import AuditModel

# Create your models here.

User = settings.AUTH_USER_MODEL


class Story(AuditModel):
    title = models.CharField(max_length=100, blank=False)
    slug = models.CharField(max_length=150, blank=False)
    content = models.TextField(blank=False)
    is_anonymous = models.BooleanField(default=False)
    disable_comments = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ("updated_at",)
        verbrose_name = "story"
        verbrose_name_plural = "stories"

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.upvotes.all


class Upvote(AuditModel):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="upvotes",
    )

    def __str__(self):
        return self.upvoted_by.username


class Comment(AuditModel):
    content = models.TextField(blank=False)
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    def __str__(self):
        return "Comment on {} by {}".format(self.story.title, self.create_by)
