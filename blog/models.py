from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tags(models.Model):
    name=models.CharField(max_length=30,unique=True)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='DR','DRAFT'
        PUBLISHED='PUB','PUBLISHED'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish_date',unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    content = models.TextField()
    tags = models.ManyToManyField(Tags, related_name='posts', blank=True)
    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.DRAFT
    )

    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(max_length=300, blank=True, help_text="A short snippet")


    class Meta:
        ordering = ['-publish_date', '-created_at']

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='blog_images/%Y/%m/%d/')
    caption = models.CharField(
        max_length=200, blank=True, help_text='Optional image caption'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.post.title}'

    