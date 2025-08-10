from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
# Create your models here.

options = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published', blank=True, null=True)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=options, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ['-published']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(
        CustomUser,
        related_name='comments',
        on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
