from django.db import models
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.utils.timezone import now


class Text(models.Model):
    class Meta:
        permissions = (
            ('my_edit_text', 'CUSTOM Can edit text'),
            ('my_publish_text', 'CUSTOM Can publish text'),
            ('my_unpublish_text', 'CUSTOM Can unpublish text'),
            ('my_remove_text', 'CUSTOM Can remove text'),
        )

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    file_name = models.CharField(max_length=200)
    file_name_mini = models.CharField(max_length=200)
    published = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def votes(self):
        return self.vote_set.aggregate(votes=Coalesce(models.Sum('vote'), 0))['votes']

    @property
    def comments(self):
        return self.comment_set.count()

    def publish(self):
        self.published = True
        self.published_at = now()
        self.save()

    def unpublish(self):
        self.published = False
        self.save()

    def add_processed_image(self, file_name, file_name_mini):
        self.file_name = file_name
        self.file_name_mini = file_name_mini
        self.processed = True
        self.save()

    def upvote(self, user):
        Vote.objects.filter(text=self, user=user).delete()
        Vote(text=self, user=user, vote=1).save()

    def downvote(self, user):
        Vote.objects.filter(text=self, user=user).delete()
        Vote(text=self, user=user, vote=-1).save()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(default=1)

    def __str__(self):
        return 'User: ' + self.user.username +\
               '; Text: ' + self.text.title +\
               '; Vote: ' + str(self.vote)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User: ' + self.user.username +\
               '; Text: ' + self.text.title +\
               '; Published at: ' + str(self.published_at)
