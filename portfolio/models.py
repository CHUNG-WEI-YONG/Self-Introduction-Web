from django.db import models

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

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



    
        