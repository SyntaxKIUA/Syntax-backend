from django.db import models

from apps.users.models import User


class Post(models.Model):
    pass


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='User',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Post",
    )
    comment = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="Parent Comment",
    )

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_at']


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes_on_posts'
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='likes_on_comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Liked by {self.user},  for {self.post}, and Like_id {self.id}"

    def clean(self):
        if not self.post and not self.comment:
            raise ValueError(
                'A Like must be associated with either a post or a comment, not both.'
            )
        if self.post and self.comment:
            raise ValueError(
                'A Like cannot be associated with both a post and a comment simultaneously.'
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post_like',
                condition=models.Q(post__isnull=False),
            ),
            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_user_comment_like',
                condition=models.Q(comment__isnull=False),
            ),
        ]
