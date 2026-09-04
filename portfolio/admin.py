from django.contrib import admin
from .models import TechCategory,Technology,Project
# Register your models here.

@admin.register(TechCategory)
class TechCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'is_learning')
    list_filter = ('category', 'is_learning', 'proficiency')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)  # 提供双栏多选穿梭框 UI

