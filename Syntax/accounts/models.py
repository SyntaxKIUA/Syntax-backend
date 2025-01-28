from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)


class Post(models.Model):
    title = models.CharField(max_length=255)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_on_posts')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes_on_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.post and not self.comment:
            raise ValueError('A Like must be associated with either a post or a comment, not both.')
        if self.post and self.comment:
            raise ValueError('A Like cannot be associated with both a post and a comment simultaneously.')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post_like',
                condition=models.Q(post__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_user_comment_like',
                condition=models.Q(comment__isnull=False)
            )
        ]


