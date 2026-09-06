from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import itertools

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
    slug = models.SlugField(max_length=255, unique=True, blank=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # 解决重名导致的 UNIQUE constraint failed
        original_slug = self.slug
        for x in itertools.count(1):
            if not Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                break
            self.slug = f"{original_slug}-{x}"

        super().save(*args, **kwargs)

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

    