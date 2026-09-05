from django.db import models
from django.utils.text import slugify 
import itertools

# Create your models here.
class TechCategory(models.Model):
    name=models.CharField(max_length=50,unique=True)
    order=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Tech Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Technology(models.Model):
    name=models.CharField(max_length=50)
    class ProficiencyLevel(models.TextChoices):
        BEGINNER = 'BEG', 'Beginner'
        INTERMEDIATE = 'INT', 'Intermediate'
        ADVANCED = 'ADV', 'Advanced'
        EXPERT = 'EXP', 'Expert'

    category=models.ForeignKey(
        TechCategory,
        on_delete=models.CASCADE,
        related_name='technologies'
    )

    proficiency = models.CharField(
        max_length=3,
        choices=ProficiencyLevel.choices,
        default=ProficiencyLevel.BEGINNER
    )
    is_learning=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Technologies"


    def __str__(self):
        return self.name


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'PLANNING', 'Planning'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        PAUSED = 'PAUSED', 'Paused'

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS
    )
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    technologies = models.ManyToManyField(
        Technology,
        related_name='projects',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # 如果没有填写 slug，或者 slug 为空，则从 title 自动生成
        if not self.slug:
            self.slug = slugify(self.title)

        # 确保 slug 全局唯一，若重复则自动拼接递增数字（如 project-1, project-2）
        original_slug = self.slug
        for x in itertools.count(1):
            # 查询是否存在同名 slug（排除当前对象本身，方便编辑更新）
            if not Project.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                break
            self.slug = f"{original_slug}-{x}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



    
        