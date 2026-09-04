from django.core.management.base import BaseCommand
from agent.rag_service import sync_knowledge_base

class Command(BaseCommand):
    help = 'Sync portfolio projects, technologies, and blog posts into ChromaDB'

    def handle(self,*args,**opts):
        self.stdout.write(self.style.NOTICE('Starting knowledge extraction...'))
        count=sync_knowledge_base()
        self.stdout.write(
        self.style.SUCCESS(
            f'Successfully indexed {count} items into ChromaDB vector store!'
        )
    )
