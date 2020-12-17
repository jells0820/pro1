from datetime import datetime, date

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=1000)
    question_tag = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date asked', auto_now_add=True)
    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('a_list', kwargs={'question_id': self.id})

class Article(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = RichTextField(blank=True, null=True)
    #description = models.TextField()
    pub_date = models.DateTimeField('date written', auto_now_add=True)
    article_tag = models.CharField(max_length=1000)
    likes = models.ManyToManyField(User, related_name='article_likes')
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    def was_published_today(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_absolute_url(self):
        return reverse('article', args=(str(self.question.id), str(self.id)))

    def total_likes(self):
        return self.likes.count()

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    pinterest_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('index')

'''
class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.article.title, self.user.username)
'''
