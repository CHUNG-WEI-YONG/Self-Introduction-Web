from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from blog.models import Post
from portfolio.models import Project
from .services import KnowLedgeBaseService

kb_service=KnowLedgeBaseService()

@receiver(post_save, sender=Post)
def sync_post_to_chroma(sender, instance, created, **kwargs):
    if instance.status == Post.Status.PUBLISHED:
        combined_content = f"{instance.summary or ''}\n\n{instance.content}"
        kb_service.upsert_entity(
            entity_type="blog",
            entity_id=instance.id,
            title=instance.title,
            content=combined_content,
            url=f"/blog/{instance.slug}/"
        )
    else:
        kb_service.delete_entity(entity_type="blog", entity_id=instance.id)

@receiver(post_delete, sender=Post)
def delete_post_from_chroma(sender, instance, **kwargs):
    kb_service.delete_entity(entity_type="blog", entity_id=instance.id)

@receiver(post_save, sender=Project)
def sync_project_to_chroma(sender, instance, created, **kwargs):
    tech_stack = ", ".join([t.name for t in instance.technologies.all()])
    combined_content = f"Tech Stack: {tech_stack}\nDescription: {instance.description}"
    kb_service.upsert_entity(
        entity_type="project",
        entity_id=instance.id,
        title=instance.title,
        content=combined_content,
        url=f"/portfolio/projects/{instance.slug}/"
    )

@receiver(post_delete, sender=Project)
def delete_project_from_chroma(sender, instance, **kwargs):
    kb_service.delete_entity(entity_type="project", entity_id=instance.id)

